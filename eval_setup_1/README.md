**Getting started**

The results can be reproduced by following the steps:


1. get the local IP of your machine using ifconfig on linux or ipconfig on windows cmd for example.
2. get all IPs in local network using your machine's local IP. For example if your local IP is 192.168.178.xxx then call

```bash
./getIPs 192.168.178.
```

The output looks like:

```bash
user@hostmachine-Virtual-Machine:~/Desktop/rt_monitoring_system/eval_1$ ./getIPs.sh 192.168.178.
192.168.178.90
192.168.178.1
192.168.178.91
192.168.178.92
192.168.178.84
.
.
```

3. Pick one local IP to run ping_loop with. For example 192.168.178.90

```
./ping_loop.sh 192.168.178.90

host,latency
192.168.178.91,240.580
192.168.178.91,104.554
```

4. If you got similar output, then call ebpf_program.py and ping_loop.sh in separate terminals.
  
  pipe the each output to a csv file

```
sudo python3 ./ebpf_program.py 192.168.178.90 > ebpf_results_1node_native.csv
```

```
./ping_loop.sh 192.168.178.90 > ping_results_1node_native.csv
```

5. Finally, plot the results by running

```
python3 plot_setup1.py
```

If you change the names of the csv files make sure to modify them inside plot_setup1.py too.
