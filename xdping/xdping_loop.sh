#!/bin/bash
LOOP_END=5

# TODO: replace the ip below with your target node
ip="192.168.178.26"

echo "host,latencyPing,latencyXDPing"

for _ in $(seq 1 $LOOP_END);
do
  sudo ./xdping -I eth0 -c 1 $ip | grep -E "^64 bytes from" | awk '{print $4, $7}' \
  | sed -e 's/time=//' | tr '\n' ',' | sed 's/,/ /g' | awk -F ' ' '{print $1,$2,$4}' | sed 's/://g' | sed 's/ /,/g'

done
