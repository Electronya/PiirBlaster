import paho.mqtt.client as mqtt

from irEmitter import IrEmitter
from remote import Remote

class Device(mqtt.Client):
    # Constructor
    def __init__(self, config, logger):
        super().__init__(client_id=config['location']+'.'+config['name'])
        self.config = config
        self.logger = logger
        self.logger.info('Creating device: %s.%s', config['location'], config['name'])

        self.irEmitter = None
        self._initRemote(self.config['remote']['manufacturer'], self.config['remote']['model'])
        self._initMqttClient(self.config['user'], self.config['broker'], self.config['lastWill'])

    # Init the device remote
    def _initRemote(self, manufacturer, model):
        self.logger.info('%s.%s: Initializing remote %s', self.config['location'], self.config['name'], model)
        self.remote = Remote(self.logger, manufacturer, model)

    # Init device mqtt client
    def _initMqttClient(self, user, broker, lastWill):
        self.will_set(lastWill['topic'], lastWill['payload'],
            lastWill['qos'], lastWill['retain'])
        self.username_pw_set(user['name'], user['password'])
        self.tls_set()
        self.tls_insecure_set(True)
        self.logger.info('%s.%s: Connecting to %s:%d', self.config['location'], self.config['name'],
            broker['ip'], broker['port'])
        self.logger.debug('%s.%s: Connecting as %s with password %s', self.config['location'], self.config['name'],
            user['name'], user['password'])
        self.connect(broker['ip'], port=broker['port'])
        self.loop_start()

    # On connection
    def on_connect(self, client, usrData, flags, rc):
        self.logger.info('%s.%s: Connected', self.config['location'], self.config['name'])
        self.logger.debug('%s.%s: rc %s', self.config['location'], self.config['name'], str(rc))

    # On disconnect
    def on_disconnect(self, client, usrData, rc):
        self.logger.info('%s.%s: Disconnected', self.config['location'], self.config['name'])
        self.logger.debug('%s.%s: rc %s', self.config['location'], self.config['name'], str(rc))

    # On message
    def on_message(self, client, usrData, msg):
        self.logger.info('%s.%s: Message recieved %s', self.config['location'], self.config['name'], msg.topic)

    # On publish
    def on_publish(self, client, usrData, mid):
        self.logger.info('%s.%s: Message published', self.config['location'], self.config['name'])
        self.logger.debug('%s.%s: mid %s', self.config['location'], self.config['name'], str(mid))

    # On subscribe
    def on_subscribe(self, client, usrData, mid, grantedQoS):
        self.logger.info('%s.%s: Subscibed with QoS %d', self.config['location'], self.config['name'], grantedQoS)
        self.logger.debug('%s.%s: mid ', self.config['location'], self.config['name'], str(mid))

    # On log
    def on_log(self, client, usrData, logLevel, logMsg):
        switcher = {
            'MQTT_LOG_INFO': self.logger.info,
            'MQTT_LOG_NOTICE': self.logger.info,
            'MQTT_LOG_WARNING': self.logger.warning,
            'MQTT_LOG_ERR': self.logger.error,
            'MQTT_LOG_DEBUG': self.logger.debug,
        }
        switcher[logLevel]('%s.%s: %s', self.config['location'], self.config['name'], logMsg)

    # Link IR emitter
    def linkIrEmitter(self, irEmitter):
        self.irEmitter = irEmitter
