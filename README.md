# RT network monitoring system based on eBPF

This is a real-time network monitoring system for Linux. It combines the power of the Linux kernel's eBPF technology with the flexibility of the Prometheus monitoring system.

**Table of Contents**

                
+ [Implementation](implementation)
    + DataAggregator
    + DataVisualizer
+ [Evaluation1 EBPF](eval_setup_1)
+ [Evaluation2 EBPF](eval_setup_2)
+ [Evaluation3 XDP](xdping)
#


###Images

Flow diagram:

![](images/software_architecture.drawio.png)


Software architecture:

![](images/software_architecture_uml.png)


Network graph example:

![](images/network_graph.png)


Latency evaluation on GCP testbed:

![](images/latency_gcp.png)


Latency evaluation on native machine testbed:

![](images/latency_native.png)


Latency evaluation on docker testbed:

![](images/latency_docker.png)


----
###End
