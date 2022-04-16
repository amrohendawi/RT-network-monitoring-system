#!/bin/bash

LOOP_END=10
# TODO: replace the ip addresses below with the ones from the testbed network (GCP/Docker/Native)
ips=(172.27.0.3 172.27.0.2 172.27.0.4)

echo "host,latency"
# paste the IPs as an array and get results piped to csv file
for _ in $(seq 1 $LOOP_END); do
  for ip in "${ips[@]}"; do
    ping -c 1 $ip | grep "64 bytes from" | awk '{print $4}{print $7}' | cut -d":" -f1 | \
    sed -e 's/,/./g' | sed ':begin;$!N;s/\n/,/;tbegin' | sed -e 's/time=//g' &
  done
  sleep 3;
done