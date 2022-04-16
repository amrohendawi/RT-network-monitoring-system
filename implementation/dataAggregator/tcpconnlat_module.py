#!/usr/bin/python
# @lint-avoid-python-3-compatibility-imports
#
# tcpconnlat    Trace TCP active connection latency (connect).
#               For Linux, uses BCC, eBPF. Embedded C.
#
# USAGE: tcpconnlat [-h] [-t] [-p PID] [-4 | -6]
#
# This uses dynamic tracing of kernel functions, and will need to be updated
# to match kernel changes.
#
# Copyright 2016 Netflix, Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# 19-Feb-2016   Brendan Gregg   Created this.
# 15-Mar-2021   Suresh Kumar    Added LPORT option
# 21-Dec-2021   Amro Hendawi    Added prometheus metrics exporter

from __future__ import print_function
from bcc import BPF
from socket import inet_ntop, AF_INET, AF_INET6
from struct import pack
from prometheus_client import Summary, Gauge

print("imported tcp_connlat module!")
latencyGauge = Gauge('tcp_connlat_msec', 'tcp connection latency',['saddr', 'daddr'] )

debug = 0

# define BPF program
bpf_text = """
#include <uapi/linux/ptrace.h>
#include <net/sock.h>
#include <net/tcp_states.h>
#include <bcc/proto.h>

struct info_t {
    u64 ts;
    u32 pid;
    char task[TASK_COMM_LEN];
};
BPF_HASH(start, struct sock *, struct info_t);

// separate data structs for ipv4 and ipv6
struct ipv4_data_t {
    u64 ts_us;
    u32 pid;
    u32 saddr;
    u32 daddr;
    u64 ip;
    u16 lport;
    u16 dport;
    u64 delta_us;
    char task[TASK_COMM_LEN];
};
BPF_PERF_OUTPUT(ipv4_events);

struct ipv6_data_t {
    u64 ts_us;
    u32 pid;
    unsigned __int128 saddr;
    unsigned __int128 daddr;
    u64 ip;
    u16 lport;
    u16 dport;
    u64 delta_us;
    char task[TASK_COMM_LEN];
};
BPF_PERF_OUTPUT(ipv6_events);

int trace_connect(struct pt_regs *ctx, struct sock *sk)
{
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    struct info_t info = {.pid = pid};
    info.ts = bpf_ktime_get_ns();
    bpf_get_current_comm(&info.task, sizeof(info.task));
    start.update(&sk, &info);
    return 0;
};

int trace_tcp_rcv_state_process(struct pt_regs *ctx, struct sock *skp)
{
    // will be in TCP_SYN_SENT for handshake
    if (skp->__sk_common.skc_state != TCP_SYN_SENT)
        return 0;

    // check start and calculate delta
    struct info_t *infop = start.lookup(&skp);
    if (infop == 0) {
        return 0;   // missed entry or filtered
    }

    u64 ts = infop->ts;
    u64 now = bpf_ktime_get_ns();

    u64 delta_us = (now - ts) / 1000ul;

#ifdef MIN_LATENCY
    if ( delta_us < DURATION_US ) {
        return 0; // connect latency is below latency filter minimum
    }
#endif

    // pull in details
    u16 family = 0, lport = 0, dport = 0;
    family = skp->__sk_common.skc_family;
    lport = skp->__sk_common.skc_num;
    dport = skp->__sk_common.skc_dport;

    // emit to appropriate data path
    if (family == AF_INET) {
        struct ipv4_data_t data4 = {.pid = infop->pid, .ip = 4};
        data4.ts_us = now / 1000;
        data4.saddr = skp->__sk_common.skc_rcv_saddr;
        data4.daddr = skp->__sk_common.skc_daddr;
        data4.lport = lport;
        data4.dport = ntohs(dport);
        data4.delta_us = delta_us;
        __builtin_memcpy(&data4.task, infop->task, sizeof(data4.task));
        ipv4_events.perf_submit(ctx, &data4, sizeof(data4));

    } else /* AF_INET6 */ {
        struct ipv6_data_t data6 = {.pid = infop->pid, .ip = 6};
        data6.ts_us = now / 1000;
        bpf_probe_read_kernel(&data6.saddr, sizeof(data6.saddr),
            skp->__sk_common.skc_v6_rcv_saddr.in6_u.u6_addr32);
        bpf_probe_read_kernel(&data6.daddr, sizeof(data6.daddr),
            skp->__sk_common.skc_v6_daddr.in6_u.u6_addr32);
        data6.lport = lport;
        data6.dport = ntohs(dport);
        data6.delta_us = delta_us;
        __builtin_memcpy(&data6.task, infop->task, sizeof(data6.task));
        ipv6_events.perf_submit(ctx, &data6, sizeof(data6));
    }
    start.delete(&skp);

    return 0;
}
"""

# initialize BPF
b = BPF(text=bpf_text)
b.attach_kprobe(event="tcp_v4_connect", fn_name="trace_connect")
b.attach_kprobe(event="tcp_v6_connect", fn_name="trace_connect")

b.attach_kprobe(event="tcp_rcv_state_process",
    fn_name="trace_tcp_rcv_state_process")

# process event
start_ts = 0

def print_ipv4_event(cpu, data, size):
    event = b["ipv4_events"].event(data)
    latencyGauge.labels( inet_ntop(AF_INET, pack("I", event.saddr)),
                    inet_ntop(AF_INET, pack("I", event.daddr))
                    ).set(float(event.delta_us) / 1000)

def print_ipv6_event(cpu, data, size):
    event = b["ipv6_events"].event(data)
    latencyGauge.labels( inet_ntop(AF_INET6, event.saddr),
                    inet_ntop(AF_INET6, event.daddr)
                    ).set(float(event.delta_us) / 1000)

# read events
b["ipv4_events"].open_perf_buffer(print_ipv4_event)
b["ipv6_events"].open_perf_buffer(print_ipv6_event)

def run_tcpconnlat():
    while 1:
        try:
            b.perf_buffer_poll()
        except KeyboardInterrupt:
            exit()