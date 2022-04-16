#!/bin/bash

# adjust loop end for quick tests. set it to 10 before final benchmark collection
LOOP_END=100
target_ip=192.168.178.91
echo "host,latency"
for _ in $(seq 1 $LOOP_END);
do
    ping -c 1 -W 1 $target_ip | grep -Po '(PING |min/avg/max/stddev = )\K.*?(?=\s|\/)' | sed -e 's/,/./g' | sed ':begin;$!N;s/\n/,/;tbegin' | grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3},[0-9]+\.[0-9]+' &
    sleep 3;
done