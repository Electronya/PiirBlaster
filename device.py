import paho.mqtt.client as mqtt
import os
import json

from ircodec.command import CommandSet

class Device(mqtt.Client):
    # Constants
    STATUS_TOPIC = 'status'
    CMD_TOPIC = 'command'
    RESULT_TOPIC = 'result'

    ONLINE_MSG = 'ONLINE'
    OFFLINE_MSG = 'OFFLINE'
    SUCCESS_MSG = 'done'
    ERROR_MSG = 'unsupported'

    # Constructor
    def __init__(self, logger, mqttConfig, devConfig, isNew=False):
        super().__init__(client_id=devConfig['location']+'.'+devConfig['name'])
        self.config = devConfig
        self.logger = logger

        if isNew:
            self.logger.info(f"{self.config['location']}.{self.config['name']}: Creating new device")
            self.commandSet = CommandSet(emitter_gpio=self.config['commandSet']['emitterGpio'],
                receiver_gpio=self.config['commandSet']['receiverGpio'],
                description=self.config['commandSet']['description'])
        else:
            self.logger.info(f"{self.config['location']}.{self.config['name']}: Loading existing device")
            self.commandSet = CommandSet.load(os.path.join('./commandSets',
                self.config['commandSet']['manufacturer'], self.config['commandSet']['model'] + '.json'))

        self.baseTopic = self.config['topicPrefix']+'/'+self.config['location']+'/'+self.config['name']+'/'
        self._initMqttClient(mqttConfig['user'], mqttConfig['broker'], self.config['lastWill'])

    # Init device mqtt client
    def _initMqttClient(self, user, broker, lastWill):
        willTopic = self.baseTopic + self.STATUS_TOPIC

        # Set client settings
        self.will_set(willTopic, self.OFFLINE_MSG, lastWill['qos'], lastWill['retain'])
        self.username_pw_set(user['name'], user['password'])
        self.tls_set()
        self.tls_insecure_set(True)

        self.logger.info(f"{self.config['location']}.{self.config['name']}: Connecting to {broker['ip']}:{broker['port']}")
        self.logger.debug(f"{self.config['location']}.{self.config['name']}: Connecting as {user['name']} with password {user['password']}")

        # Connect to broker
        self.connect(broker['ip'], port=broker['port'])

        # Start network loop
        self.loop_start()

    # Publish command result
    def _publishCmdResult(self, success):
        resultTopic = self.baseTopic + self.RESULT_TOPIC
        if success:
            self.logger.info(f"{self.config['location']}.{self.config['name']}: Command sent")
            self.publish(resultTopic, payload=self.SUCCESS_MSG)
        else:
            self.logger.info(f"{self.config['location']}.{self.config['name']}: Command unsupported")
            self.publish(resultTopic, payload=self.ERROR_MSG)

    # On connection
    def on_connect(self, client, usrData, flags, rc):
        self.logger.info(f"{self.config['location']}.{self.config['name']}: Connected")
        self.logger.debug(f"{self.config['location']}.{self.config['name']}: rc {rc}")

        # Publish ONLINE status
        statusTopic = self.baseTopic + self.STATUS_TOPIC
        self.publish(statusTopic, payload=self.ONLINE_MSG, qos=1, retain=True)

        # Subscribing to command topic
        cmdTopic = self.baseTopic + self.CMD_TOPIC
        self.subscribe(cmdTopic)

    # On disconnect
    def on_disconnect(self, client, usrData, rc):
        self.logger.info(f"{self.config['location']}.{self.config['name']}: Disconnected")
        self.logger.debug(f"{self.config['location']}.{self.config['name']}: rc {rc}")

    # On message
    def on_message(self, client, usrData, msg):
        receivedMsg = msg.payload.decode('utf-8')
        self.logger.info(f"{self.config['location']}.{self.config['name']}: Message recieved {receivedMsg}")
        for i in range(0,4):
            self.logger.debug(f"{self.config['location']}.{self.config['name']}: Sending packet #{i}")
            # TODO: Manage unsupported command
            self.commandSet.emit(receivedMsg, emit_gap=self.config['commandSet']['packetGap'])
        self._publishCmdResult(True)

    # On publish
    def on_publish(self, client, usrData, mid):
        self.logger.info(f"{self.config['location']}.{self.config['name']}: Message published")
        self.logger.debug(f"{self.config['location']}.{self.config['name']}: mid {mid}")

    # On subscribe
    def on_subscribe(self, client, usrData, mid, grantedQoS):
        self.logger.info(f"{self.config['location']}.{self.config['name']}: Subscibed with QoS {grantedQoS}")
        self.logger.debug(f"{self.config['location']}.{self.config['name']}: mid {mid}")

    # On log
    def on_log(self, client, usrData, logLevel, logMsg):
        switcher = {
            mqtt.MQTT_LOG_INFO: self.logger.info,
            mqtt.MQTT_LOG_NOTICE: self.logger.info,
            mqtt.MQTT_LOG_WARNING: self.logger.warning,
            mqtt.MQTT_LOG_ERR: self.logger.error,
            mqtt.MQTT_LOG_DEBUG: self.logger.debug,
        }
        switcher[logLevel](f"{self.config['location']}.{self.config['name']}: {logMsg}")

    # Set device config
    def setConfig(self, config):
        self.logger(f"{self.config['location']}.{self.config['name']}: Setting device config to {config}")
        self.config = config

    # Get device config
    def getConfig(self):
        self.logger(f"{self.config['location']}.{self.config['name']}: Getting device config")
        return self.config

    # Get command list
    def getCommandList(self):
        self.logger(f"{self.config['location']}.{self.config['name']}: Getting command list")
        return self.commandSet.to_json()

    # Add a command
    def addCommand(self, command, description):
        self.logger(f"{self.config['location']}.{self.config['name']}: Adding command {command} to command set")
        self.commandSet.add(command, description=description)

    # Delete a command
    def deleteCommand(self, command):
        self.logger(f"{self.config['location']}.{self.config['name']}: Deleting command {command} from command set")
        self.commandSet.remove(command)

    # Save device Config
    def saveConfig(self):
        result = {'result': 'fail'}
        try:
            with open('./config/devices.json') as configFile:
                deviceConfigs = json.loads(configFile.read())
                devConfigItr = filter(lambda device: device['name'] == self.config['name'], deviceConfigs)
                deviceConfig = next(devConfigItr, None)
                if deviceConfig is not None:
                    deviceConfig = self.config
                else:
                    deviceConfigs.append(self.config)
                devConfigsContent = json.dumps(deviceConfigs, sort_keys=True, indent=2)
                configFile.write(devConfigsContent)
            result['result'] = 'success'
        except EnvironmentError:
            result['message'] = 'Error accessing devices configuration file!!'
        return result

    # Save device command set
    def saveCommandSet(self):
        result = {'result': 'fail'}
        try:
            self.commandSet.save_as(os.path.join('./commandSets', self.config['commandSet'] + '.json'))
            result['result'] = 'success'
        except EnvironmentError:
            result['message'] = 'Error accessing command set file'
        return result
