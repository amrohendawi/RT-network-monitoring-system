**Getting started**

Requirements:

| Testbed | Requirement |
| ------ | ------ |
| Docker | Docker-cli latest |
| GCP | gcp cli, Ubuntu 18.04 LTS, 4GB RAM, 2 vCPU |

On each testbed environment the following dependencies are required:

1. [BCC tools](https://github.com/iovisor/bcc)
2. python3
3. gnu inetutils-ping

To install gnu inetutils-ping on cloud instances:

```bash
# on cloud instances remove iputils-ping
sudo apt-get remove iputils-ping

# then install gnu inetutils-ping
wget http://ftp.de.debian.org/debian/pool/main/i/inetutils/inetutils-ping_1.9.4-7+deb10u1_amd64.deb
sudo dpkg -i inetutils-ping_1.9.4-7+deb10u1_amd64.deb
```

- To setup the testbed environment for docker run

  ```bash
  # You can modify num_nodes variable inside testbed_docker.sh to choose how many container instances to create
  sudo ./testbed_docker.sh
  ```

- To setup the tesbed environment for gcp create n instances manually and ssh into one of them.


**Running the evaluation**

<details><summary>Native testbed</summary>

The results can be reproduced by following the steps:

1. get the local IP of your machine using ifconfig on linux or ipconfig on windows cmd for example.
2. get all IPs in local network using your machine's local IP. For example if your local IP is 192.168.178.xxx then call

```bash
./getIPs 192.168.178.
```

The output looks like:

```bash
user@hostmachine-Virtual-Machine:~/Desktop/rt_monitoring_system/eval_setup_2$ ./getIPs.sh 192.168.178.
192.168.178.90
192.168.178.1
192.168.178.91
192.168.178.92
192.168.178.84
.
.
```

3. Copy the local IPs of the target nodes inside ping_loop_setup2.sh and run it

```
./ping_loop_setup2.sh

host,latency
192.168.178.91,240.580
192.168.178.91,104.554
```

4. If you got similar output, then call ebpf_program_setup2.py and ping_loop_setup2.sh in separate terminals.

  pipe each output to a csv file.

  copy the target IPs to ebpf_program_setup2.py (the variable at the top of the code).

```
sudo python3 ./ebpf_program_setup2.py > ebpf_results_native.csv
```

```
./ping_loop_setup2.sh > ping_results_native.csv
```

5. Finally, plot the results by running

```
python3 plot_setup2.py
```

If you change the names of the csv files make sure to modify them inside plot_setup2.py too.
</details>


<details><summary>Docker testbed</summary>

The results can be reproduced by following the steps:

1. setup the testbed environment for docker run

  ```bash
  # You can modify num_nodes variable inside testbed_docker.sh to choose how many container instances to create
  sudo ./testbed_docker.sh
  ```

  An example output looks like:

  ```
  sudo ./testbed_docker.sh
  .
  .
  created 5 nodes. their IP addresses are:
  172.18.0.2 172.18.0.4 172.18.0.5 172.18.0.3 172.18.0.6
  please copy the IPs array above to ping_loop_setup2.sh
  ```


2. Copy the local IPs of the target nodes inside ping_loop_setup2.sh and run it

```
./ping_loop_setup2.sh

host,latency
172.18.0.2,240.580
172.18.0.3,104.554
```

  You can also modify the varial LOOP_END.

4. If you got similar output, then call ebpf_program_setup2.py and ping_loop_setup2.sh in separate terminals.

  pipe each output to a csv file.

  copy the target IPs to ebpf_program_setup2.py (the variable at the top of the code).

```
sudo python3 ./ebpf_program_setup2.py > ebpf_results_docker.csv
```

```
./ping_loop_setup2.sh > ping_results_docker.csv
```

5. Finally, plot the results by running

```
python3 plot_setup2.py
```

If you change the names of the csv files make sure to modify them inside plot_setup2.py too.
</details>


