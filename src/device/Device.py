from logging import Logger
import paho.mqtt.client as mqtt
from ircodec.command import CommandSet

import os

from exceptions import CommandNotFound, \
    CommandFileAccess


class Device():
    # Constants
    STATUS_TOPIC = 'status'
    CMD_TOPIC = 'command'
    RESULT_TOPIC = 'result'

    ONLINE_MSG = 'ONLINE'
    OFFLINE_MSG = 'OFFLINE'
    SUCCESS_MSG = 'done'
    ERROR_MSG = 'unsupported'

    def __init__(self, logger, appConfig, devConfig, isNew=False):
        """
        Constructor.

        Params:
            logger:         The logger.
            appConfig:      The application configuration.
            devConfig:      The device configuration.
            isNew:          The flag indicating if the device is a new one,
                            or an existing commande set exists.
        """
        self.config = devConfig
        self.logger = logger.getLogger(f"{devConfig['location']}."
                                       f"{devConfig['name']}")

        if isNew:
            self.logger.info('Creating new device')
            name = self.config['commandSet']['model']
            emitter = self.config['commandSet']['emitterGpio']
            receiver = self.config['commandSet']['receiverGpio']
            description = self.config['commandSet']['description']
            self.commandSet = CommandSet(name, emitter_gpio=emitter,
                                         receiver_gpio=receiver,
                                         description=description)
        else:
            self.logger.info('Loading existing device')
            manufacturer = self.config['commandSet']['manufacturer']
            model = self.config['commandSet']['model']
            try:
                self.commandSet = CommandSet.load(os.path.join('./commandSets',
                                                  manufacturer, f"{model}."
                                                  f"json"))
            except Exception:
                raise CommandFileAccess('unable to access the command file.')

        self.baseTopic = f"{self.config['topicPrefix']}/{self.config['location']}/{self.config['name']}/"   # noqa: E501

        self._initMqttClient(appConfig.getUserName(),
                             appConfig.getUserPassword(),
                             appConfig.getBrokerHostname(),
                             appConfig.getBrokerPort())

    def _initMqttClient(self, userName, userPassword,
                        brokerIp, brokerPort):
        """
        Initialize the MQTT client.

        Params:
            userName:           The user name for connecting to the broker.
            userPassword:       The user password for connecting to the broker.
            brokerHostname:     The broker hostname.
            brokerPort:         The broker port.
        """
        self.client = mqtt.Client(client_id=f"{self.config['location']}."
                                  f"{self.config['name']}")
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
        self.client.on_publish = self._on_publish
        self.client.on_subscribe = self._on_subscribe
        self.client.on_log = self._on_log

        willTopic = self.baseTopic + self.STATUS_TOPIC
        self.client.will_set(willTopic, self.OFFLINE_MSG,
                             self.config['lastWill']['qos'],
                             self.config['lastWill']['retain'])
        self.client.username_pw_set(userName, userPassword)
        # TODO: Implement switch for secure or not.
        # self.client.tls_set()
        # self.client.tls_insecure_set(True)

        self.logger.info(f"Connecting to {brokerIp}:{brokerPort}")
        self.logger.debug(f"Connecting as {userName} with password "
                          f"{userPassword}")
        self.client.connect(brokerIp, port=brokerPort)

    def _publishCmdResult(self, success):
        """
        Publish a command result.

        Params:
            success:            The flag indicating to send success
                                or fail result.
        """
        resultTopic = self.baseTopic + self.RESULT_TOPIC
        if success:
            self.logger.info('Command sent')
            self.client.publish(resultTopic, payload=self.SUCCESS_MSG)
        else:
            self.logger.warning('Command unsupported')
            self.client.publish(resultTopic, payload=self.ERROR_MSG)

    def _on_connect(self, client, usrData, flags, rc):
        """
        The on connect callback.

        Params:
            client:         The mqtt client.
            usrData:        User data.
            flags:          The connection flags.
            rc:             The connection result.
        """
        self.logger.info('Connected')
        self.logger.debug(f"rc {rc}")
        statusTopic = self.baseTopic + self.STATUS_TOPIC
        self.client.publish(statusTopic, payload=self.ONLINE_MSG,
                            qos=1, retain=True)

        cmdTopic = self.baseTopic + self.CMD_TOPIC
        self.client.subscribe(cmdTopic)

    def _on_disconnect(self, client, usrData, rc):
        """
        The on disconnect callback.

        Params:
            client:         The mqtt client.
            usrData:        User data.
            flags:          The connection flags.
            rc:             The connection result.
        """
        self.logger.info('Disconnected')
        self.logger.debug(f"rc {rc}")

    def _on_message(self, client, usrData, msg):
        """
        The on message callback.

        Params:
            client:         The mqtt client.
            usrData:        User data.
            msg:            The message data.
        """
        reuslt = True
        receivedMsg = msg.payload.decode('utf-8')
        self.logger.info(f"Message recieved {receivedMsg}")
        try:
            for i in range(0, 4):
                self.logger.debug(f"Sending packet #{i}")
                gap = self.config['commandSet']['packetGap']
                self.commandSet.emit(receivedMsg, emit_gap=gap)
        except KeyError as e:
            self.logger.warning(str(e))
            reuslt = False
        self._publishCmdResult(reuslt)

    def _on_publish(self, client, usrData, mid):
        """
        The on publish callback.

        Params:
            client:         The mqtt client.
            usrData:        User data.
            mid:            The message ID that have been published.
        """
        self.logger.info('Message published')
        self.logger.debug(f"mid {mid}")

    def _on_subscribe(self, client, usrData, mid, grantedQoS):
        """
        The on subscribe callback.

        Params:
            client:         The mqtt client.
            usrData:        User data.
            mid:            The message ID that have been published.
            grantedQoS:     The granted QoS for the subcription.
        """
        self.logger.info(f"Subscibed with QoS {grantedQoS}")
        self.logger.debug(f"mid {mid}")

    def _on_log(self, client, usrData, logLevel, logMsg):
        """
        The on log callback.

        Params:
            client:         The mqtt client.
            usrData:        User data.
            logLevel:       The level of the log message.
            logMsg:         The log message.
        """
        switcher = {
            mqtt.MQTT_LOG_INFO: self.logger.info,
            mqtt.MQTT_LOG_NOTICE: self.logger.info,
            mqtt.MQTT_LOG_WARNING: self.logger.warning,
            mqtt.MQTT_LOG_ERR: self.logger.error,
            mqtt.MQTT_LOG_DEBUG: self.logger.debug,
        }
        switcher[logLevel](logMsg)

    def startLoop(self):
        """
        Start the network loop.
        """
        self.client.loop_start()

    def stopLoop(self):
        """
        Stop the network loop.
        """
        self.client.loop_stop()
        self.client.disconnect()

    def getName(self):
        """
        Get the device name.

        Return:
            The device name.
        """
        return self.config['name']

    def getLocation(self):
        """
        Get the device location,

        Return:
            The device location.
        """
        return self.config['location']

    def getConfig(self):
        """
        Get the device configuration.

        Return:
            The device configuration.
        """
        self.logger.debug('Getting device config')
        return self.config

    def setConfig(self, config):
        """
        Set the device configuration.

        Params:
            config:         The device configuration.
        """
        self.logger.debug(f"Setting device config to {config}")
        self.config = config

    def getCommandList(self):
        """
        Get the device command list.

        Return:
            The device command list.
        """
        self.logger.debug('Getting command list')
        cmdSetJson = self.commandSet.to_json()
        return cmdSetJson['commands'].keys()

    def addCommand(self, command, description):
        """"
        Add a command to the device.

        Params:
            command:            The command name.
            description:        The command description.
        """
        self.logger.debug(f"Adding command {command} to command set")
        self.commandSet.add(command, description=description)

    def deleteCommand(self, command):
        """
        Delete a command from the device.

        Params:
            command:            The command name.

        Raise:
            CommandNotFound if the requested command is not supported.
        """
        self.logger.debug(f"Deleting command {command} from command set")
        try:
            self.commandSet.remove(command)
        except KeyError:
            raise CommandNotFound(command)

    def saveCommandSet(self):
        """
        Save the device command set.

        Raise:
            CommandFileAccess if the save operation fail.
        """
        try:
            self.commandSet.save_as(os.path.join('./commandSets',
                                    self.config['commandSet']['manufacturer'],
                                    f"{self.config['commandSet']['model']}"
                                    f".json"))
        except Exception:
            raise CommandFileAccess('unable to access the command file.')
