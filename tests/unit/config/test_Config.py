import json
import logging
from unittest import TestCase
from unittest.mock import call, Mock, mock_open, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from config import Config                               # noqa: E402
from exceptions import MqttFileAccess, \
    HardwareFileAccess                                  # noqa: E402


class TestConfig(TestCase):
    """
    Config test cases.
    """
    def setUp(self):
        """
        Test cases setup.
        """
        with open('./tests/unit/config/mqtt.json') as mqttConfFile:
            self.mqttConfStr = mqttConfFile.read()
            self.mqttConfig = json.loads(self.mqttConfStr)

        with open('./tests/unit/config/hardware.json') as hardConfFile:
            self.hardConfStr = hardConfFile.read()
            self.hardConfig = json.loads(self.hardConfStr)

    def test_constructorMqttFileError(self):
        """
        The constructor must raise a MqttFileAccess error if
        access to the MQTT configuration file fails.
        """
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedConf, \
                self.assertRaises(MqttFileAccess) as context:
            mockedConf.side_effect = \
                [OSError, mock_open(read_data=self.hardConfStr).return_value]
            config = Config(logging)                # noqa: F841
            self.assertTrue('unable to access mqtt configuraion file'
                            in str(context.exception),
                            'Config failed to raise a MqttFileAccess '
                            'exception when access to the MQTT '
                            'configuration access failed.')

    def test_constructorHardFileError(self):
        """
        The constructor must raise a HardwareFileAccess error if
        access to the hardware configuration file fails.
        """
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedConf, \
                self.assertRaises(HardwareFileAccess) as context:
            mockedConf.side_effect = [mockedConf.return_value, OSError]
            appConfig = Config(logging)                # noqa: F841
            self.assertTrue('unable to access hardware configuraion file'
                            in str(context.exception),
                            'Config failed to raise a HardwareFileAccess '
                            'exception when access to the hardware '
                            'configuration access failed.')

    def test_contructorLoadConfigFiles(self):
        """
        The constructor must load the MQTT and hardware configuration files.
        """
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedConf:
            mockedConf.side_effect = \
                [mockedConf.return_value,
                 mock_open(read_data=self.hardConfStr).return_value]
            appConfig = Config(logging)                    # noqa: F841
            mockedConf.assert_any_call(f"{Config.CONFIG_PATH}/"
                                       f"{Config.MQTT_CONFIG_FILE}")
            mockedConf.assert_any_call(f"{Config.CONFIG_PATH}/"
                                       f"{Config.HW_CONFIG_FILE}")

    def test_getBrokerHostname(self):
        """
        The getBrokerHostname must return the broker hostname/IP.
        """
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedConf:
            mockedConf.side_effect = \
                [mockedConf.return_value,
                 mock_open(read_data=self.hardConfStr).return_value]
            appConfig = Config(logging)
            self.assertEqual(appConfig.getBrokerHostname(),
                             self.mqttConfig['broker']['hostname'],
                             'Config getBrokerHostname failed to '
                             'return the current broker hostname.')

    def test_setBrokerHostname(self):
        """
        The setBrokerHostname must update the MQTT configuration with the
        new hostname.
        """
        newHostname = 'new hostname'
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedConf:
            mockedConf.side_effect = \
                [mockedConf.return_value,
                 mock_open(read_data=self.hardConfStr).return_value]
            appConfig = Config(logging)
            appConfig.setBrokerHostname(newHostname)
            self.assertEqual(appConfig.getBrokerHostname(), newHostname,
                             'Config setBrokerHostname failed to '
                             'update the current broker hostname.')

    def test_getBrokerPort(self):
        """
        The getBrokerPort must return the broker port.
        """
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedConf:
            mockedConf.side_effect = \
                [mockedConf.return_value,
                 mock_open(read_data=self.hardConfStr).return_value]
            appConfig = Config(logging)
            self.assertEqual(appConfig.getBrokerPort(),
                             self.mqttConfig['broker']['port'],
                             'Config getBrokerPort failed to '
                             'return the current broker port.')

    def test_setBrokerPort(self):
        """
        The setBrokerPort must update the MQTT configuration with the
        new port.
        """
        newPort = 'new port'
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedConf:
            mockedConf.side_effect = \
                [mockedConf.return_value,
                 mock_open(read_data=self.hardConfStr).return_value]
            appConfig = Config(logging)
            appConfig.setBrokerPort(newPort)
            self.assertEqual(appConfig.getBrokerPort(), newPort,
                             'Config setBrokerPort failed to '
                             'update the current broker port.')

    def test_getUserName(self):
        """
        The getUserName must return the MQTT user name.
        """
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedConf:
            mockedConf.side_effect = \
                [mockedConf.return_value,
                 mock_open(read_data=self.hardConfStr).return_value]
            appConfig = Config(logging)
            self.assertEqual(appConfig.getUserName(),
                             self.mqttConfig['user']['name'],
                             'Config getUserName failed to '
                             'return the current user name.')

    def test_setUserName(self):
        """
        The setUserName must update the MQTT configuration with the
        new user name.
        """
        newUserName = 'new user'
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedConf:
            mockedConf.side_effect = \
                [mockedConf.return_value,
                 mock_open(read_data=self.hardConfStr).return_value]
            appConfig = Config(logging)
            appConfig.setUserName(newUserName)
            self.assertEqual(appConfig.getUserName(), newUserName,
                             'Config setUserName failed to '
                             'update the current user name.')

    def test_getUserPassword(self):
        """
        The getUserPassword must return the MQTT user password.
        """
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedConf:
            mockedConf.side_effect = \
                [mockedConf.return_value,
                 mock_open(read_data=self.hardConfStr).return_value]
            appConfig = Config(logging)
            self.assertEqual(appConfig.getUserPassword(),
                             self.mqttConfig['user']['password'],
                             'Config getUserPassword failed to '
                             'return the current user password.')

    def test_setUserPassword(self):
        """
        The setUserPassword must update the MQTT configuration with the
        new user password.
        """
        newUserPassword = 'new password'
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedConf:
            mockedConf.side_effect = \
                [mockedConf.return_value,
                 mock_open(read_data=self.hardConfStr).return_value]
            appConfig = Config(logging)
            appConfig.setUserPassword(newUserPassword)
            self.assertEqual(appConfig.getUserPassword(), newUserPassword,
                             'Config setUserPassword failed to '
                             'update the current user password.')

    def test_getMqttConfig(self):
        """
        The getMqttConfig must return the MQTT configuration.
        """
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedConf:
            mockedConf.side_effect = \
                [mockedConf.return_value,
                 mock_open(read_data=self.hardConfStr).return_value]
            appConfig = Config(logging)
            self.assertEqual(appConfig.getMqttConfig(), self.mqttConfig,
                             'Config getMqttConfig failed to '
                             'return the current MQTT configuration.')

    def test_setMqttConfig(self):
        """
        The setMqttConfig must update the MQTT configuration with the
        full new configuration.
        """
        newConfig = self.mqttConfig.copy()
        newConfig['broker']['hostname'] = 'new hostname'
        newConfig['broker']['port'] = 'new port'
        newConfig['user']['name'] = 'new username'
        newConfig['user']['password'] = 'new password'
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedConf:
            mockedConf.side_effect = \
                [mockedConf.return_value,
                 mock_open(read_data=self.hardConfStr).return_value]
            appConfig = Config(logging)
            appConfig.setMqttConfig(newConfig)
            self.assertEqual(appConfig.getMqttConfig(), newConfig,
                             'Config setMqttConfig failed to '
                             'update the current MQTT configuration.')

    def test_saveMqttConfigFail(self):
        """
        The saveMqttConfig method must raise an MqttFileAccess when the write
        operation fails.
        """
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedConf:
            mockedConf.side_effect = \
                [mockedConf.return_value,
                 mock_open(read_data=self.hardConfStr).return_value]
            appConfig = Config(logging)
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedMqttConf:
            mockedMqttConf.side_effect = OSError
            with self.assertRaises(MqttFileAccess) as context:
                appConfig.saveMqttConfig()
                self.assertTrue('unable to access mqtt configuraion file'
                                in str(context.exception),
                                'Config saveMqtt/config failed to raise a '
                                'MqttFileAccess exception when access to '
                                'the MQTT configuration access failed.')

    def test_saveMqttConfigWriting(self):
        """
        The saveMqttConfig method must write the current active configuration
        to the MQTT configuration file.
        """
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedConf:
            mockedConf.side_effect = \
                [mockedConf.return_value,
                 mock_open(read_data=self.hardConfStr).return_value]
            appConfig = Config(logging)
        newMqttConfig = self.mqttConfig.copy()
        newMqttConfig['broker']['hostname'] = 'new host'
        newMqttConfig['user']['name'] = 'new user'
        newMqttConfig['user']['password'] = 'new password'
        appConfig.setMqttConfig(newMqttConfig)
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedMqttConfig:
            appConfig.saveMqttConfig()
            mockedMqttConfig \
                .assert_called_once_with(os.path.join(appConfig.CONFIG_PATH,
                                                      appConfig.MQTT_CONFIG_FILE))      # noqa: E501
            mockedMqttConfig() \
                .write.assert_called_once_with(json.dumps(newMqttConfig,
                                                          sort_keys=True,
                                                          indent=2))

    def test_getInputName(self):
        """
        The getInputName method must return the PiirBlaster input name.
        """
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedConf:
            mockedConf.side_effect = \
                [mockedConf.return_value,
                 mock_open(read_data=self.hardConfStr).return_value]
            appConfig = Config(logging)
            self.assertEqual(appConfig.getInputName(),
                             self.hardConfig['in']['name'],
                             'Config getInputName failed to return '
                             'the PiirBlaster input name.')

    def test_getInputGpioId(self):
        """
        The getInputGpioId method must return the Raspberry Pi input ID.
        """
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedConf:
            mockedConf.side_effect = \
                [mockedConf.return_value,
                 mock_open(read_data=self.hardConfStr).return_value]
            appConfig = Config(logging)
            self.assertEqual(appConfig.getInputGpioId(),
                             self.hardConfig['in']['gpioId'],
                             'Config getInputGpioId failed to return '
                             'the current Raspberry Pi input ID.')

    def test_setInputGpioId(self):
        """
        The setInputGpioId method must update the hardware configuration
        with the new Raspberry Pi input ID.
        """
        newGpioId = 17
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedConf:
            mockedConf.side_effect = \
                [mockedConf.return_value,
                 mock_open(read_data=self.hardConfStr).return_value]
            appConfig = Config(logging)
            appConfig.setInputGpioId(newGpioId)
            self.assertEqual(appConfig.getInputGpioId(), newGpioId,
                             'Config setInputGpio failed to update '
                             'the current Raspberry Pi input ID.')

    def test_getOutputCount(self):
        """
        The getOutputCount method must return the total number
        of usable output channel.
        """
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedConf:
            mockedConf.side_effect = \
                [mockedConf.return_value,
                 mock_open(read_data=self.hardConfStr).return_value]
            appConfig = Config(logging)
            self.assertEqual(appConfig.getOutputCount(),
                             len(self.hardConfig['out']),
                             'Config getOutputCount failed to return '
                             'the number of usable output channel.')

    def test_getOutputNameOutRange(self):
        """
        The getOutputName method must raise an IndexError exception if
        the given index is out of range.
        """
        testIdxes = [6, 10, -7, -10]
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedConf:
            mockedConf.side_effect = \
                [mockedConf.return_value,
                 mock_open(read_data=self.hardConfStr).return_value]
            appConfig = Config(logging)
        for testIdx in testIdxes:
            with self.assertRaises(IndexError) as context:
                appConfig.getOutputName(testIdx)
                self.assertTrue('list index out of range'
                                in str(context.exception),
                                'Config getOutputName failed to raise '
                                'an IndexError if the given output index '
                                'is out of range.')

    def test_getOutputNameInRange(self):
        """
        The getOutputName method must return the PiirBlaster
        output name of the output at the given index. If the given
        index is within range.
        """
        testIdxes = [0, 5, -1, -6, 3, -2]
        expectedNames = ['OUT0', 'OUT5', 'OUT5', 'OUT0', 'OUT3', 'OUT4']
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedConf:
            mockedConf.side_effect = \
                [mockedConf.return_value,
                 mock_open(read_data=self.hardConfStr).return_value]
            appConfig = Config(logging)
        for idx in range(len(testIdxes)):
            self.assertEqual(appConfig.getOutputName(testIdxes[idx]),
                             expectedNames[idx],
                             'Config getOutputName failed to return '
                             'the PiirBlaster name of the output at '
                             'the given index.')

    def test_getOutputGpioIdOutRange(self):
        """
        The getOutputGpioId method must raise an IndexError exception if
        the given index is out of range.
        """
        testIdxes = [6, 10, -7, -10]
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedConf:
            mockedConf.side_effect = \
                [mockedConf.return_value,
                 mock_open(read_data=self.hardConfStr).return_value]
            appConfig = Config(logging)
        for testIdx in testIdxes:
            with self.assertRaises(IndexError) as context:
                appConfig.getOutputGpioId(testIdx)
                self.assertTrue('list index out of range'
                                in str(context.exception),
                                'Config getOutputGpioId failed to raise '
                                'an IndexError if the given output index '
                                'is out of range.')

    def test_getOutputGpioIdInRange(self):
        """
        The getOutputGpioId method must return the Raspberry Pi
        gpio ID of the output at the given index. If the given
        index is within range.
        """
        testIdxes = [0, 5, -1, -6, 3, -2]
        expectedNames = [4, 9, 9, 4, 22, 10]
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedConf:
            mockedConf.side_effect = \
                [mockedConf.return_value,
                 mock_open(read_data=self.hardConfStr).return_value]
            appConfig = Config(logging)
        for idx in range(len(testIdxes)):
            self.assertEqual(appConfig.getOutputGpioId(testIdxes[idx]),
                             expectedNames[idx],
                             'Config getOutputGpioId failed to return '
                             'the Raspberry Pi gpio ID of the output at '
                             'the given index.')

    def test_setOutputGpioIdOutRange(self):
        """
        The setOutputGpioId method must raise an IndexError exception if
        the given index is out of range.
        """
        testIdxes = [6, 10, -7, -10]
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedConf:
            mockedConf.side_effect = \
                [mockedConf.return_value,
                 mock_open(read_data=self.hardConfStr).return_value]
            appConfig = Config(logging)
        for testIdx in testIdxes:
            with self.assertRaises(IndexError) as context:
                appConfig.setOutputGpioId(testIdx, 10)
                self.assertTrue('list index out of range'
                                in str(context.exception),
                                'Config getOutputGpioId failed to raise '
                                'an IndexError if the given output index '
                                'is out of range.')

    def test_setOutputGpioIdInRange(self):
        """
        The setOutputGpioId method must update the Raspberry Pi
        gpio ID of the output at the given index. If the given
        index is within range.
        """
        testIdxes = [0, 5, -1, -6, 3, -2]
        expectedIds = [12, 10, 11, 3, 14, 6]
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedConf:
            mockedConf.side_effect = \
                [mockedConf.return_value,
                 mock_open(read_data=self.hardConfStr).return_value]
            appConfig = Config(logging)
        for idx in range(len(testIdxes)):
            appConfig.setOutputGpioId(testIdxes[idx], expectedIds[idx])
            self.assertEqual(appConfig.getOutputGpioId(testIdxes[idx]),
                             expectedIds[idx],
                             'Config setOutputGpioId failed to update '
                             'the Raspberry Pi gpio ID of the output at '
                             'the given index.')

    def test_getHwConfig(self):
        """
        The getHwConfig must return the hardware configuration.
        """
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedConf:
            mockedConf.side_effect = \
                [mockedConf.return_value,
                 mock_open(read_data=self.hardConfStr).return_value]
            appConfig = Config(logging)
            self.assertEqual(appConfig.getHwConfig(), self.hardConfig,
                             'Config getHwConfig failed to '
                             'return the current hardware configuration.')

    def test_setHwConfig(self):
        """
        The setHwConfig must update the hardware configuration with the
        full new configuration.
        """
        newConfig = self.hardConfig.copy()
        newConfig['in']['gpioId'] = 12
        newConfig['out'][2]['gpioId'] = 13
        newConfig['out'][3]['gpioId'] = 14
        newConfig['out'][5]['gpioId'] = 22
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedConf:
            mockedConf.side_effect = \
                [mockedConf.return_value,
                 mock_open(read_data=self.hardConfStr).return_value]
            appConfig = Config(logging)
            appConfig.setHwConfig(newConfig)
            self.assertEqual(appConfig.getHwConfig(), newConfig,
                             'Config sethardwareConfig failed to '
                             'update the current hardware configuration.')

    def test_saveHwConfigFail(self):
        """
        The saveHwConfig method must raise an HardwareFileAccess when the write
        operation fails.
        """
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedConf:
            mockedConf.side_effect = \
                [mockedConf.return_value,
                 mock_open(read_data=self.hardConfStr).return_value]
            appConfig = Config(logging)
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedMqttConf:
            mockedMqttConf.side_effect = OSError
            with self.assertRaises(HardwareFileAccess) as context:
                appConfig.saveHwConfig()
                self.assertTrue('unable to access hardware configuraion file'
                                in str(context.exception),
                                'Config saveHwconfig failed to raise a '
                                'HardwareFileAccess exception when access to '
                                'the Hw configuration access failed.')

    def test_saveHwConfigWriting(self):
        """
        The saveHwConfig method must write the current active configuration
        to the hardware configuration file.
        """
        with patch('builtins.open', mock_open(read_data=self.mqttConfStr)) \
                as mockedConf:
            mockedConf.side_effect = \
                [mockedConf.return_value,
                 mock_open(read_data=self.hardConfStr).return_value]
            appConfig = Config(logging)
        newConfig = self.hardConfig.copy()
        newConfig['in']['gpioId'] = 12
        newConfig['out'][2]['gpioId'] = 13
        newConfig['out'][3]['gpioId'] = 14
        newConfig['out'][5]['gpioId'] = 22
        appConfig.setHwConfig(newConfig)
        with patch('builtins.open', mock_open(read_data=self.hardConfStr)) \
                as mockedHwConfig:
            appConfig.saveHwConfig()
            mockedHwConfig \
                .assert_called_once_with(os.path.join(appConfig.CONFIG_PATH,
                                                      appConfig.HW_CONFIG_FILE))    # noqa: E501
            mockedHwConfig() \
                .write.assert_called_once_with(json.dumps(newConfig,
                                                          sort_keys=True,
                                                          indent=2))
