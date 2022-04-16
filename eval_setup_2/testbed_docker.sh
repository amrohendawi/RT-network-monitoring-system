#!/bin/bash
num_nodes=3
network_name=setup2

# cleanup from past runs
for instance in $(seq 1 $num_nodes)
do
    docker stop node-$instance
done

res=$(docker network ls | grep $network_name)
if ! [ -z "$res" ];
then
    docker network rm $network_name
fi
#####################

# create docker network with mtu higher than 1500
docker network create --driver=bridge \
-o "com.docker.network.driver.mtu"="3000" \
-o "com.docker.network.bridge.host_binding_ipv4"="0.0.0.0" \
-o "com.docker.network.bridge.enable_icc"="true" $network_name

for instance in $(seq 1 $num_nodes)
do
    docker run -it -d --rm --name node-$instance --network $network_name alpine
done

for instance in $(seq 1 $num_nodes)
do
    echo assigned IP address for node-$instance:
    docker exec node-$instance ip addr show eth0
    echo ""
done

echo "created ${num_nodes} nodes. their IP addresses are:"
echo "copy the array below to ebpf_program_setup2.py:"
ip_addresses=$(docker network inspect --format '{{range .Containers}}{{.IPv4Address}}{{end}}' setup2 | sed 's/\/16/ /g' | sed 's/ $//')
for ip in $ip_addresses
do
    echo -n "'$ip',"
done
echo
echo "copy the IPs array below to ping_loop_setup2.sh"
echo $ip_addresses