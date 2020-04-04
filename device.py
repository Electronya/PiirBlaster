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
        self.logger.info(f"Creating device: {devConfig['location']}.{devConfig['name']}")

        self.irEmitter = linkedEmitter
        self.baseTopic = self.devConfig['topicPrefix']+'/'+self.devConfig['location']+'/'+self.devConfig['name']+'/'

        self._initRemote(self.devConfig['remote']['manufacturer'], self.devConfig['remote']['model'])
        self._initMqttClient(mqttConfig['user'], mqttConfig['broker'], self.devConfig['lastWill'])

    # Init the device remote
    def _initRemote(self, manufacturer, model):
        self.logger.info(f"{self.devConfig['location']}.{self.devConfig['name']}: Initializing remote {model}")
        self.remote = Remote(self.logger, manufacturer, model)

    # Init device mqtt client
    def _initMqttClient(self, user, broker, lastWill):
        willTopic = self.baseTopic + self.STATUS_TOPIC

        # Set client settings
        self.will_set(willTopic, self.OFFLINE_MSG, lastWill['qos'], lastWill['retain'])
        self.username_pw_set(user['name'], user['password'])
        self.tls_set()
        self.tls_insecure_set(True)

        self.logger.info(f"{self.devConfig['location']}.{self.devConfig['name']}: Connecting to {broker['ip']}:{broker['port']}")
        self.logger.debug(f"{self.devConfig['location']}.{self.devConfig['name']}: Connecting as {user['name']} with password {user['password']}")

        # Connect to broker
        self.connect(broker['ip'], port=broker['port'])

        # Start network loop
        self.loop_start()

    # Publish command result
    def _publishCmdResult(self, success):
        resultTopic = self.baseTopic + self.RESULT_TOPIC
        if success:
            self.logger.info(f"{self.devConfig['location']}.{self.devConfig['name']}: Command supported")
            self.publish(resultTopic, payload=self.SUCCESS_MSG)
        else:
            self.logger.info(f"{self.devConfig['location']}.{self.devConfig['name']}: Command unsupported")
            self.publish(resultTopic, payload=self.ERROR_MSG)

    # Process command
    def _processCommad(self, command):
        self.logger.info(f"{self.devConfig['location']}.{self.devConfig['name']}: Processing command {command}")
        cmdBitTimings = self.remote.generateCmd(command)
        self.logger.debug(f"{self.devConfig['location']}.{self.devConfig['name']}: Command bit timings\n{cmdBitTimings}")
        if cmdBitTimings is None:
            self._publishCmdResult(False)
        else:
            self._publishCmdResult(True)

    # On connection
    def on_connect(self, client, usrData, flags, rc):
        self.logger.info(f"{self.devConfig['location']}.{self.devConfig['name']}: Connected")
        self.logger.debug(f"{self.devConfig['location']}.{self.devConfig['name']}: rc {rc}")

        # Publish ONLINE status
        statusTopic = self.baseTopic + self.STATUS_TOPIC
        self.publish(statusTopic, payload=self.ONLINE_MSG, qos=1, retain=True)

        # Subscribing to command topic
        cmdTopic = self.baseTopic + self.CMD_TOPIC
        self.subscribe(cmdTopic)


    # On disconnect
    def on_disconnect(self, client, usrData, rc):
        self.logger.info(f"{self.devConfig['location']}.{self.devConfig['name']}: Disconnected")
        self.logger.debug(f"{self.devConfig['location']}.{self.devConfig['name']}: rc {rc}")

    # On message
    def on_message(self, client, usrData, msg):
        receivedMsg = msg.payload.decode('utf-8')
        self.logger.info(f"{self.devConfig['location']}.{self.devConfig['name']}: Message recieved {receivedMsg}")
        self._processCommad(receivedMsg)

    # On publish
    def on_publish(self, client, usrData, mid):
        self.logger.info(f"{self.devConfig['location']}.{self.devConfig['name']}: Message published")
        self.logger.debug(f"{self.devConfig['location']}.{self.devConfig['name']}: mid {mid}")

    # On subscribe
    def on_subscribe(self, client, usrData, mid, grantedQoS):
        self.logger.info(f"{self.devConfig['location']}.{self.devConfig['name']}: Subscibed with QoS {grantedQoS}")
        self.logger.debug(f"{self.devConfig['location']}.{self.devConfig['name']}: mid {mid}")

    # On log
    def on_log(self, client, usrData, logLevel, logMsg):
        switcher = {
            'MQTT_LOG_INFO': self.logger.info,
            'MQTT_LOG_NOTICE': self.logger.info,
            'MQTT_LOG_WARNING': self.logger.warning,
            'MQTT_LOG_ERR': self.logger.error,
            'MQTT_LOG_DEBUG': self.logger.debug,
        }
        switcher[logLevel](f"{self.devConfig['location']}.{self.devConfig['name']}: {logMsg}")

    # Link IR emitter
    def linkIrEmitter(self, irEmitter):
        self.irEmitter = irEmitter
