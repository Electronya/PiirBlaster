import paho.mqtt.client as mqtt
from ircodec.command import CommandSet

import os


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
    def __init__(self, logger, appConfig, devConfig, isNew=False):
        super().__init__(client_id=f"{devConfig['location']}."
                         f"{devConfig['name']}")
        self.config = devConfig
        self.logger = logger.getLogger(f"{devConfig['location']}."
                                       f"{devConfig['name']}")

        if isNew:
            self.logger.info('Creating new device')

            emitter = self.config['commandSet']['emitterGpio']
            receiver = self.config['commandSet']['receiverGpio']
            description = self.config['commandSet']['description']
            self.commandSet = CommandSet(emitter_gpio=emitter,
                                         receiver_gpio=receiver,
                                         description=description)
        else:
            self.logger.info('Loading existing device')

            manufacturer = self.config['commandSet']['manufacturer']
            model = self.config['commandSet']['model']
            self.commandSet = CommandSet.load(os.path.join('./commandSets',
                                              manufacturer, f"{model}.json"))

        self.baseTopic = f"{self.config['topicPrefix']}/{self.config['location']}/{self.config['name']}/"   # noqa: E501

        self._initMqttClient(appConfig.getUserName(),
                             appConfig.getUserPassword(),
                             appConfig.getBrokerHostname(),
                             appConfig.getBrokerPort(),
                             self.config['lastWill'])

    # Init device mqtt client
    def _initMqttClient(self, userName, userPassword,
                        brokerIp, brokerPort, lastWill):
        willTopic = self.baseTopic + self.STATUS_TOPIC

        # Set client settings
        self.will_set(willTopic, self.OFFLINE_MSG,
                      lastWill['qos'], lastWill['retain'])
        self.username_pw_set(userName, userPassword)
        # TODO: Implement switch for secure or not.
        # self.tls_set()
        # self.tls_insecure_set(True)

        self.logger.info(f"Connecting to {brokerIp}:{brokerPort}")
        self.logger.debug(f"Connecting as {userName} with password "
                          f"{userPassword}")

        # Connect to broker
        self.connect(brokerIp, port=brokerPort)

    # Publish command result
    def _publishCmdResult(self, success):
        resultTopic = self.baseTopic + self.RESULT_TOPIC
        if success:
            self.logger.info('Command sent')
            self.publish(resultTopic, payload=self.SUCCESS_MSG)
        else:
            self.logger.warning('Command unsupported')
            self.publish(resultTopic, payload=self.ERROR_MSG)

    # On connection
    def on_connect(self, client, usrData, flags, rc):
        self.logger.info('Connected')
        self.logger.debug(f"rc {rc}")

        # Publish ONLINE status
        statusTopic = self.baseTopic + self.STATUS_TOPIC
        self.publish(statusTopic, payload=self.ONLINE_MSG, qos=1, retain=True)

        # Subscribing to command topic
        cmdTopic = self.baseTopic + self.CMD_TOPIC
        self.subscribe(cmdTopic)

    # On disconnect
    def on_disconnect(self, client, usrData, rc):
        self.logger.info('Disconnected')
        self.logger.debug(f"rc {rc}")

    # On message
    def on_message(self, client, usrData, msg):
        receivedMsg = msg.payload.decode('utf-8')
        self.logger.info(f"Message recieved {receivedMsg}")
        for i in range(0, 4):
            self.logger.debug(f"Sending packet #{i}")
            # TODO: Manage unsupported command
            gap = self.config['commandSet']['packetGap']
            self.commandSet.emit(receivedMsg, emit_gap=gap)
        self._publishCmdResult(True)

    # On publish
    def on_publish(self, client, usrData, mid):
        self.logger.info('Message published')
        self.logger.debug(f"mid {mid}")

    # On subscribe
    def on_subscribe(self, client, usrData, mid, grantedQoS):
        self.logger.info(f"Subscibed with QoS {grantedQoS}")
        self.logger.debug(f"mid {mid}")

    # On log
    def on_log(self, client, usrData, logLevel, logMsg):
        switcher = {
            mqtt.MQTT_LOG_INFO: self.logger.info,
            mqtt.MQTT_LOG_NOTICE: self.logger.info,
            mqtt.MQTT_LOG_WARNING: self.logger.warning,
            mqtt.MQTT_LOG_ERR: self.logger.error,
            mqtt.MQTT_LOG_DEBUG: self.logger.debug,
        }
        switcher[logLevel](logMsg)

    # Get device name
    def getName(self):
        return self.config['name']

    # Get device location
    def getLocation(self):
        return self.config['location']

    # Set device config
    def setConfig(self, config):
        self.logger.debug(f"Setting device config to {config}")
        self.config = config

    # Get device config
    def getConfig(self):
        self.logger.debug('Getting device config')
        return self.config

    # Get command list
    def getCommandList(self):
        self.logger.debug('Getting command list')
        return self.commandSet.to_json()

    # Add a command
    def addCommand(self, command, description):
        self.logger.debug(f"Adding command {command} to command set")
        self.commandSet.add(command, description=description)

    # Delete a command
    def deleteCommand(self, command):
        self.logger.debug(f"Deleting command {command} from command set")
        self.commandSet.remove(command)

    # Save device command set
    def saveCommandSet(self):
        result = {'result': 'failed'}
        try:
            self.commandSet.save_as(os.path.join('./commandSets',
                                    f"{self.config['commandSet']}.json"))
            result['result'] = 'success'
        except EnvironmentError:
            result['message'] = 'Error accessing command set file'
        return result
