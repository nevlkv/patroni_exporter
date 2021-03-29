import json
import os
import time
import requests
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server,MetricsHandler
from urllib.parse import urlparse

port = os.environ["patroni_exporter_port"]
patroni_host = os.environ["patroni_host"]
patroni_port = os.environ["patroni_port"]

class CustomCollector():
   
    def collect(self):
        g = GaugeMetricFamily("patroni_status", 'Patroni status', labels=['cluster','name','value'])
        resp = requests.get('http://{}:{}'.format(patroni_host, patroni_port))
        resp.raise_for_status()
        js=resp.json()
        cluster=js['patroni']['scope']
        g.add_metric([cluster,'{}'.format('xlog'),'value'],'{}'.format(js['xlog']['location']))
        standbys=js["replication"]
        for standby in standbys:
           for key in standby:
             g.add_metric([cluster,'{}'.format(key),'{}'.format(standby[key])],1)
        yield g

if __name__ == '__main__':
    http_server=start_http_server(int(port))
    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(1)

