#!/bin/bash

for ip in $1.{1..254}; do

  ping -c 1 -W 16 $ip | grep "64 bytes from" | awk '{print $4}' | cut -d":" -f1 &

done
