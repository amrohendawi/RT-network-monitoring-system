#!/usr/bin/env python3
# Before running this script, install required Pythons package manager:
#   sudo apt update && sudo apt install -y python-pip
# Then install required packages:
#   pip install pandas matplotlib

from turtle import color
import matplotlib.pyplot as plt
import pandas as df

def plot_line(ebpf_data, ping_data):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_title('latency comparison of eBPF and ping on native machines')
    ax.set_xlabel('samples count')
    ax.set_ylabel('latency (ms)')
    print('p %s e %s' % (ping_data, ebpf_data))
    ax.plot(ping_data, label='ping', linewidth=1)
    ax.plot(ebpf_data, label='eBPF', linewidth=1)
    ax.legend(fontsize=10)
    plt.show()
    print(f'ping: mean(%s) std(%s)' % (ping_data.mean(), ping_data.std()))
    print(f'ebpf: mean(%s) std(%s)' % (ebpf_data.mean(), ebpf_data.std()))

def plot_stacked_bars(data_ping, data_ebpf):
    # create a figure
    fig = plt.figure(figsize=(10, 5))
    # create a subplot
    ax = fig.add_subplot(111)
    # create a stacked bar histogram
    ax.hist([data_ping, data_ebpf],
            bins=5,
            label=['non-eBPF', 'eBPF'],
            stacked=True,
            histtype='bar',
            color=['#1f77b4', '#ff7f0e'])
    ax.set_xlabel('Number of samples')
    ax.set_ylabel('Latency')
    ax.set_title('Latency [ms]')
    ax.legend()
    plt.show()
    plt.close(fig)

ebpf_res = df.read_csv('ebpf_results_1node_native.csv', delimiter=',').head(100)
ping_res = df.read_csv('ping_results_1node_native.csv', delimiter=',').head(100)
ips_ping = ping_res['host'].unique() 
ips_ebpf = ebpf_res['host'].unique()
plot_line(ebpf_res['latency'], ping_res['latency'])
ebpf_sorted = ebpf_res.sort_values('latency', ascending=False)
ping_sorted = ping_res.sort_values('latency', ascending=False)
print('ebpf_sorted: %s' % (ebpf_sorted[:10]))
print('ping_sorted: %s' % (ping_sorted[:10]))

plt.clf()