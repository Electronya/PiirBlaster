import paho.mqtt.client as mqtt

from irEmitter import IrEmitter
from remote import Remote

class Device(mqtt.Client):
    # Constants
    STATUS_TOPIC = 'status'
    CMD_TOPIC = 'command'
    RESULT_TOPIC = 'result'

    ONLINE_MSG = 'ONLINE'
    OFFLINE_MSG = 'OFFLINE'
    SUCCESS_MSG = 'success'
    ERROR_MSG = 'unsupported'

    # Constructor
    def __init__(self, devConfig, mqttConfig, linkedEmitter, logger):
        super().__init__(client_id=devConfig['location']+'.'+devConfig['name'])
        self.devConfig = devConfig
        self.logger = logger
        self.logger.info('Creating device: %s.%s', devConfig['location'], devConfig['name'])

        self.irEmitter = linkedEmitter
        self.baseTopic = self.devConfig['topicPrefix']+'/'+self.devConfig['location']+'/'+self.devConfig['name']+'/'

        self._initRemote(self.devConfig['remote']['manufacturer'], self.devConfig['remote']['model'])
        self._initMqttClient(mqttConfig['user'], mqttConfig['broker'], self.devConfig['lastWill'])

    # Init the device remote
    def _initRemote(self, manufacturer, model):
        self.logger.info('%s.%s: Initializing remote %s', self.devConfig['location'], self.devConfig['name'], model)
        self.remote = Remote(self.logger, manufacturer, model)

    # Init device mqtt client
    def _initMqttClient(self, user, broker, lastWill):
        willTopic = self.baseTopic + self.STATUS_TOPIC

        # Set client settings
        self.will_set(willTopic, self.OFFLINE_MSG, lastWill['qos'], lastWill['retain'])
        self.username_pw_set(user['name'], user['password'])
        self.tls_set()
        self.tls_insecure_set(True)

        self.logger.info('%s.%s: Connecting to %s:%d', self.devConfig['location'], self.devConfig['name'],
            broker['ip'], broker['port'])
        self.logger.debug('%s.%s: Connecting as %s with password %s', self.devConfig['location'], self.devConfig['name'],
            user['name'], user['password'])

        # Connect to broker
        self.connect(broker['ip'], port=broker['port'])

        # Start network loop
        self.loop_start()

    # Publish command result
    def _publishCmdResult(self, success):
        resultTopic = self.baseTopic + self.RESULT_TOPIC
        if success:
            self.publish(resultTopic, payload=self.SUCCESS_MSG)
        else:
            self.publish(resultTopic, payload=self.ERROR_MSG)

    # Process command
    def _processCommad(self, command):
        isSupported = self.remote.getKeyCode(command)

    # On connection
    def on_connect(self, client, usrData, flags, rc):
        self.logger.info('%s.%s: Connected', self.devConfig['location'], self.devConfig['name'])
        self.logger.debug('%s.%s: rc %s', self.devConfig['location'], self.devConfig['name'], str(rc))

        # Publish ONLINE status
        statusTopic = self.baseTopic + self.STATUS_TOPIC
        self.publish(statusTopic, payload=self.ONLINE_MSG, qos=1, retain=True)

        # Subscribing to command topic
        cmdTopic = self.baseTopic + self.CMD_TOPIC
        self.subscribe(cmdTopic)


    # On disconnect
    def on_disconnect(self, client, usrData, rc):
        self.logger.info('%s.%s: Disconnected', self.devConfig['location'], self.devConfig['name'])
        self.logger.debug('%s.%s: rc %s', self.devConfig['location'], self.devConfig['name'], str(rc))

    # On message
    def on_message(self, client, usrData, msg):
        receivedMsg = msg.payload.decode('utf-8')
        self.logger.info('%s.%s: Message recieved "%s"', self.devConfig['location'], self.devConfig['name'], receivedMsg)

    # On publish
    def on_publish(self, client, usrData, mid):
        self.logger.info('%s.%s: Message published', self.devConfig['location'], self.devConfig['name'])
        self.logger.debug('%s.%s: mid %s', self.devConfig['location'], self.devConfig['name'], str(mid))

    # On subscribe
    def on_subscribe(self, client, usrData, mid, grantedQoS):
        self.logger.info('%s.%s: Subscibed with QoS %s', self.devConfig['location'], self.devConfig['name'], str(grantedQoS))
        self.logger.debug('%s.%s: mid %s', self.devConfig['location'], self.devConfig['name'], str(mid))

    # On log
    def on_log(self, client, usrData, logLevel, logMsg):
        switcher = {
            'MQTT_LOG_INFO': self.logger.info,
            'MQTT_LOG_NOTICE': self.logger.info,
            'MQTT_LOG_WARNING': self.logger.warning,
            'MQTT_LOG_ERR': self.logger.error,
            'MQTT_LOG_DEBUG': self.logger.debug,
        }
        switcher[logLevel]('%s.%s: %s', self.devConfig['location'], self.devConfig['name'], logMsg)

    # Link IR emitter
    def linkIrEmitter(self, irEmitter):
        self.irEmitter = irEmitter
