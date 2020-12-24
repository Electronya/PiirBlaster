import os
import json

class Config:
    MODULE_ID = 'Configuration'
    CONFIG_PATH = './config/app'
    HW_CONFIG_FILE = 'hardware.json'
    MQTT_CONFIG_FILE = 'mqtt.json'

    OPEN_MQTT_CONFIG = 'Opening MQTT configuration'
    SAVE_MQTT_CONFIG = 'Saving MQTT configuration'
    ERR_SAVE_MQTT_CONFIG = 'Error accessing MQTT configuration file!!'
    OPEN_HW_CONFIG = 'Opening hardware configuration'
    SAVE_HW_CONFIG = 'Saving hardware configuration'
    ERR_SAVE_HW_CONFIG = 'Error accessing hardware configuration file!!'

    # Constructor
    def __init__(self, logger):
        self.logger = logger

        # Reading MQTT config
        self.logger.info(f"{self.MODULE_ID}: {self.OPEN_MQTT_CONFIG}")
        with open(os.path.join(self.CONFIG_PATH, self.MQTT_CONFIG_FILE)) as mqttConfig:
            self.mqttConfig = json.loads(mqttConfig.read())

        # Reading hardware config
        self.logger.info(f"{self.MODULE_ID}: {self.OPEN_HW_CONFIG}")
        with open(os.path.join(self.CONFIG_PATH, self.HW_CONFIG_FILE)) as hwConfig:
            self.hwConfig = json.loads(hwConfig.read())

    def getBrokerHostname(self):
        return self.mqttConfig['broker']['hostname']

    def setBrokerHostname(self, newIp):
        self.mqttConfig['broker']['hostname'] = newIp

    def getBrokerPort(self):
        return self.mqttConfig['broker']['port']

    def setBrokerPort(self, newPort):
        self.mqttConfig['broker']['port'] = newPort

    def getUserName(self):
        return self.mqttConfig['user']['name']

    def setMqttUserName(self, newUserName):
        self.mqttConfig['user']['name'] = newUserName

    def getUserPassword(self):
        return self.mqttConfig['user']['password']

    def setUserPassword(self, newPassword):
        self.mqttConfig['user']['password'] = newPassword

    def saveMqttConfig(self):
        self.logger.info(f"{self.MODULE_ID}: {self.SAVE_MQTT_CONFIG}")
        result = {'result': 'failed'}
        try:
            with open(os.path.join(self.CONFIG_PATH, self.MQTT_CONFIG_FILE)) as configFile:
                newContent = json.dumps(self.mqttConfig, sort_keys=True, indent=2)
                configFile.write(newContent)
            result['result'] = 'success'
        except EnvironmentError:
            result['message'] = self.ERR_SAVE_MQTT_CONFIG
            self.logger.error(f"{self.MODULE_ID}: {result['message']}")
        return result

    def getInputName(self):
        return self.hwConfig['in']['name']

    def getInputGpioId(self):
        return self.hwConfig['in']['gpioId']

    def setInputGpioId(self, newGpioId):
        self.hwConfig['in']['gpioId'] = newGpioId

    def getOutputCount(self):
        return len(self.hwConfig['out'])

    def getOuputName(self, ouputIdx):
        if ouputIdx < len(self.hwConfig['out']):
            return self.hwConfig['out'][ouputIdx]['name']
        return None

    def getOuputGpioId(self, ouputIdx):
        if ouputIdx < len(self.hwConfig['out']):
            return self.hwConfig['out'][ouputIdx]['gpioId']
        return None

    def setOutputGpioId(self, ouputIdx, newGpioId):
        if ouputIdx < len(self.hwConfig['out']):
            self.hwConfig['out'][ouputIdx]['gpioId'] = newGpioId

    def saveHwConfig(self):
        self.logger.info(f"{self.MODULE_ID}: {self.SAVE_HW_CONFIG}")
        result = {'result': 'failed'}
        try:
            with open(os.path.join(self.CONFIG_PATH, self.HW_CONFIG_FILE)) as configFile:
                newContent = json.dumps(self.hwConfig, sort_keys=True, indent=2)
                configFile.write(newContent)
            result['result'] = 'success'
        except EnvironmentError:
            result['message'] = self.ERR_SAVE_HW_CONFIG
            self.logger.error(f"{self.MODULE_ID}: {result['message']}")
        return result
