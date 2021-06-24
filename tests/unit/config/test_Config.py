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
                             self.mqttConfig['broker']['hostname'])

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
            self.assertEqual(appConfig.getBrokerHostname(), newHostname)

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
                             self.mqttConfig['broker']['port'])

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
            self.assertEqual(appConfig.getBrokerPort(), newPort)

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
                             self.mqttConfig['user']['name'])

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
            self.assertEqual(appConfig.getUserName(), newUserName)

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
                             self.mqttConfig['user']['password'])

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
            self.assertEqual(appConfig.getUserPassword(), newUserPassword)

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
            self.assertEqual(appConfig.getMqttConfig(), self.mqttConfig)

    def test_setMqttConfig(self):
        """
        The setUserPassword must update the MQTT configuration with the
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
            self.assertEqual(appConfig.getMqttConfig(), newConfig)
