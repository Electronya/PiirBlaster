import socket

import netifaces as ni
from zeroconf import IPVersion, ServiceInfo, Zeroconf

class ServiceAdvertiser:
    def __init__(self, logger):
        self.logger = logger
        self.hostname = socket.gethostname()
        self.ipAddress = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
        self.serviceProps = {
            'path': '/',
            'description': 'PirBlaster Configuration Service',
            'protocol': 'socket.io'
        }
        self.logger.info(f"svcAdvertiser: Instanciating Pirblaster service advertiser at {self.hostname}@{self.ipAddress}")
        self.serviceInfo = ServiceInfo("_pirblaster._tcp.local.",
            "Electronya PirBlaster._pirblaster._tcp.local.",
            address=[socket.inet_aton(self.ipAddress)], port=5000,
            properties=self.serviceProps, server=f"{self.hostname}.")
        self.zeroconf = Zeroconf(ip_version=IPVersion.V4Only)
    def startAdvertising(self):
        self.logger.info(f"svcAdvertiser: Registering service")
        self.zeroconf.register_service(self.serviceInfo)
    def stopAdvertising(self):
        self.logger.info(f"svcAdvertiser: Unregister service")
        self.zeroconf.unregister_all_services()
        self.zeroconf.close()
