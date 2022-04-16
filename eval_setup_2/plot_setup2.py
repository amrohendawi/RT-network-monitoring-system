#!/usr/bin/env python3
# Before running this script, install required Pythons package manager:
#   sudo apt update && sudo apt install -y python-pip
# Then install required packages:
#   pip install numpy matplotlib

from turtle import color
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import datetime as dt
import pandas as df


def plot_line(ebpf_data, ping_data, src):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_title('latency comparison of eBPF and ping on ' + src)
    ax.set_xlabel('samples count')
    ax.set_ylabel('latency (ms)')
    print('p %s e %s' % (ping_data, ebpf_data))
    ax.plot(ping_data, label='ping', linewidth=1)
    ax.plot(ebpf_data, label='eBPF', linewidth=1)
    ax.legend(fontsize=10)
    plt.show()
    print(f'ping: mean(%s) std(%s)' % (ping_data.mean(), ping_data.std()))
    print(f'ebpf: mean(%s) std(%s)' % (ebpf_data.mean(), ebpf_data.std()))

testbeds = ['gcp', 'docker', 'native']

for i in range(len(testbeds)):
    testbed = testbeds[i]
    ebpf_res = df.read_csv('ebpf_results_' + testbed + '.csv', delimiter=',').head(600)
    ping_res = df.read_csv('ping_results_' + testbed + '.csv', delimiter=',').head(600)
    plot_line(ebpf_res['latency'], ping_res['latency'], testbed)

    ebpf_sorted = ebpf_res.sort_values('latency', ascending=False)
    ping_sorted = ping_res.sort_values('latency', ascending=False)
    print('ebpf_sorted %s: %s' % (testbed, ebpf_sorted[:10]))
    print('ping_sorted %s: %s' % (testbed, ping_sorted[:10]))

plt.clf()