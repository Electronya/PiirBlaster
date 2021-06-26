import os
import json

from exceptions import HardwareFileAccess, MqttFileAccess


class Config:
    CONFIG_PATH = './config/components'
    HW_CONFIG_FILE = 'hardware.json'
    MQTT_CONFIG_FILE = 'mqtt.json'

    SAVE_MQTT_CONFIG = 'MQTT configuration saved'
    ERR_SAVE_MQTT_CONFIG = 'Error accessing MQTT configuration file!!'
    SAVE_HW_CONFIG = 'Hardware configuration saved'
    ERR_SAVE_HW_CONFIG = 'Error accessing hardware configuration file!!'

    def __init__(self, logger):
        """
        Constructor.

        Params:
            logger:         The logger getter.

        Raise:
            MqttFileAccess if the access to the mqtt configuration file fail.
            HardwareFileAccess if the access to the hardware configuration
            file fail.
        """
        self.logger = logger.getLogger('CONFIG')

        try:
            self.logger.info('Opening MQTT configuration')
            with open(os.path.join(self.CONFIG_PATH,
                      self.MQTT_CONFIG_FILE)) as mqttConfig:
                self.mqttConfig = json.loads(mqttConfig.read())
        except OSError:
            raise MqttFileAccess('unable to access mqtt configuraion file')

        try:
            self.logger.info('Opening hardware configuration')
            with open(os.path.join(self.CONFIG_PATH,
                      self.HW_CONFIG_FILE)) as hwConfig:
                self.hwConfig = json.loads(hwConfig.read())
        except OSError:
            raise HardwareFileAccess('unable to access hardware '
                                     'configuraion file')

    def getBrokerHostname(self):
        """
        Get the broker hostname/IP

        Return:
            The broker hostname/IP.
        """
        return self.mqttConfig['broker']['hostname']

    def setBrokerHostname(self, hostname):
        """
        Set the broker hostname/IP.

        Params:
            hostname:       The new hostname/IP.
        """
        self.mqttConfig['broker']['hostname'] = hostname

    def getBrokerPort(self):
        """
        Get the broker port.

        Return:
            The broker port.
        """
        return self.mqttConfig['broker']['port']

    def setBrokerPort(self, port):
        """
        Set the broker port.

        Params:
            port:       The new port.
        """
        self.mqttConfig['broker']['port'] = port

    def getUserName(self):
        """
        Get MQTT user name.

        Return:
            The MQTT user name.
        """
        return self.mqttConfig['user']['name']

    def setUserName(self, userName):
        """
        Set the MQTT user name.

        Params:
            userName:       The new user name.
        """
        self.mqttConfig['user']['name'] = userName

    def getUserPassword(self):
        """
        Get the MQTT user password.

        Return:
            The MQTT user password.
        """
        return self.mqttConfig['user']['password']

    def setUserPassword(self, password):
        """
        Set the MQTT user password.

        Params:
            password:       The new MQTT user password.
        """
        self.mqttConfig['user']['password'] = password

    def getMqttConfig(self):
        """
        Get the full MQTT configuration.

        Return:
            The full MQTT configuration.
        """
        return self.mqttConfig

    def setMqttConfig(self, config):
        """
        Set the full MQTT configuration.

        Params:
            config:         The new MQTT configuration.
        """
        self.mqttConfig = config

    def saveMqttConfig(self):
        """
        Save the MQTT configuration.

        Raise:
            MqttFileAccess if the access to the MQTT configuration file fails.
        """
        self.logger.info('Saving MQTT configuration')
        try:
            with open(os.path.join(self.CONFIG_PATH,
                      self.MQTT_CONFIG_FILE)) as configFile:
                newContent = json.dumps(self.mqttConfig, sort_keys=True,
                                        indent=2)
                configFile.write(newContent)
        except OSError as e:
            self.logger.error(str(e))
            raise MqttFileAccess()

    def getInputName(self):
        """
        Get the PiirBlaster input name.

        Return:
            The PiirBlaster input name.
        """
        return self.hwConfig['in']['name']

    def getInputGpioId(self):
        """
        Get the Raspberry Pi input ID.

        Return:
            The Raspberry Pi input ID.
        """
        return self.hwConfig['in']['gpioId']

    def setInputGpioId(self, gpioId):
        """
        TODO: validate input with the raspberry pi??.
        Set the Raspberry Pi input ID.

        Params:
            gpioId:     The new Raspberry Pi input ID.
        """
        self.hwConfig['in']['gpioId'] = gpioId

    def getOutputCount(self):
        """
        Get the output channel count.

        Return:
            The output channel count.
        """
        return len(self.hwConfig['out'])

    def getOutputName(self, ouputIdx):
        """
        Get the PiirBlaster output name.

        Params:
            outputIdx:      The index of the output channel.

        Return:
            The PiirBlaster output name.

        Raise:
            IndexError if the outputIdx is out of range.
        """
        return self.hwConfig['out'][ouputIdx]['name']

    def getOutputGpioId(self, ouputIdx):
        """
        Get the Raspberry Pi output ID.

        Params:
            outputIdx:      The index of the output channel.

        Return:
            The Raspberry Pi output ID.

        Raise:
            IndexError if the outputIdx is out of range.
        """
        return self.hwConfig['out'][ouputIdx]['gpioId']

    def setOutputGpioId(self, ouputIdx, newGpioId):
        """
        TODO: validate input with the raspberry pi??.
        Set the Raspberry Pi output ID.

        Params:
            outputIdx:       The index of the output channel.
            gpioId:          The new Raspberry Pi output ID.

        Raise:
            IndexError if the outputIdx is out of range.
        """
        self.hwConfig['out'][ouputIdx]['gpioId'] = newGpioId

    def saveHwConfig(self):
        """
        Save the hardware configuration.

        Raise:
            HardwareFileAccess if the access to the hardware configuration
            file fail.
        """
        self.logger.info('Saving hardware configuration')
        result = {'result': 'failed'}
        try:
            with open(os.path.join(self.CONFIG_PATH,
                      self.HW_CONFIG_FILE)) as configFile:
                newContent = json.dumps(self.hwConfig, sort_keys=True,
                                        indent=2)
                configFile.write(newContent)
            result['result'] = self.SAVE_HW_CONFIG
        except EnvironmentError:
            result['message'] = self.ERR_SAVE_HW_CONFIG
            self.logger.error(f"{result['message']}")
        return result
