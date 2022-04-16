This is a full-fledged network monitoring system using the following technologies:

1. Docker
2. eBPF & XDP
3. Linux kernel libraries
4. Prometheus python-exporter
5. Prometheus
6. Grafana



**Requirements**

1. [BCC tools](https://github.com/iovisor/bcc)
2. python3
3. docker-compose

**Getting started**


open two separate terminals:

1. to run the dataVisualizer

```bash
cd ./dataVisualizer
docker-compose up
```

The services are accessible at the following addresses:

| Service | Address |
| ------ | ------ |
| Prometheus | localhost:9090 |
| Grafana | localhost:3000 |
| python_exporter | localhost:9435/metrics |
| Node-exporter | localhost:9100/metrics |


To import example dashboard in Grafana use the json file exported_grafana_dashboard.json

2. to run the dataAggregator

```bash
cd ./dataAggregator
sudo python3 ./python_exporter.py
```
