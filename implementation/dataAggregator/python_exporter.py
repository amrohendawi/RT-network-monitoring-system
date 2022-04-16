from prometheus_client import start_http_server
import _thread
import tcpconnlat_module
import gethostlatency_module

def run_thread(foo, threadName):
    foo()

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    print("starting up server")
    start_http_server(9435)
    # create threads from eBPF programs as modules
    try:
        _thread.start_new_thread( run_thread, (gethostlatency_module.run_gethostlatency, "Thread-1") )
        _thread.start_new_thread( run_thread, (tcpconnlat_module.run_tcpconnlat, "Thread-2") )
    except:
        print("error creating threads")
    while 1:
        pass