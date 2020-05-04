import socket

from zeroconf import IPVersion, ServiceInfo, Zeroconf

class ServiceAdvertiser:
    def __init__(self, logger):
        self.logger = logger
        self.hostname = socket.gethostname()
        self.ipAddress = socket.gethostbyname(self.hostname)
        self.logger.info(f"svcAdvertiser: Instanciating Pirblaster service advertiser at {self.ipAddress}")
        self.serviveInfo = ServiceInfo("_pirblaster._tcp.local.",
            "Electronya PirBlaster._pirblaster._tcp.local.",
            address=[socket.inet_aton(self.ipAddress)], port=80,
            properties={'path': '/'}, server=f"{self.hostname}.local.")
        self.zeroconf = Zeroconf(ip_version=IPVersion.V4Only)
    def startAdvertising(self):
        self.logger.info(f"svcAdvertiser: Registering service")
        self.zeroconf.register_service(self.serviveInfo)
    def stopAdvertising(self):
        self.logger.info(f"svcAdvertiser: Unregister service")
        self.zeroconf.unregister_service(self.serviveInfo)
        self.zeroconf.close()
