import logging
from unittest import TestCase
from unittest.mock import Mock, patch

from ircodec.command import CommandSet
import paho.mqtt.client as mqtt

import os
import sys
sys.path.append(os.path.abspath('./src'))

from config import Config                                   # noqa: E402
from device.Device import Device                            # noqa: E402
from exceptions import DeviceFileAccess, DeviceNotFound, \
    DeviceExists                                            # noqa: E402


class TestDevice(TestCase):
    """
    Device class test cases.
    """
    def setUp(self):
        """
        Test case setup.
        """
        self.deviceConfig = {
            'name': 'testDev',
            'location': 'testLocation',
            'linkedEmitter': 'OUT0',
            'commandSet': {
                'model': 'testModel',
                'manufacturer': 'testManufacturer',
                'description': 'My test device ',
                'emitterGpio': 3,
                'receiverGpio': 6,
                'packetGap': 0.01
            },
            'topicPrefix': 'testPrefix',
            'lastWill': {
                'qos': 2,
                'retain': True
            }
        }

        self.mockedAppConfig = Mock(spec_set=Config)
        self.mockedAppConfig.getUserName.return_value = 'username'
        self.mockedAppConfig.getUserPassword.return_value = 'password'
        self.mockedAppConfig.getBrokerHostname.return_value = 'host'
        self.mockedAppConfig.getBrokerPort.return_value = 2000

        self.mockedClient = Mock(spec_set=mqtt.Client)

        self.mockedCmdSet = Mock(spec_set=CommandSet)

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    def test_constructorNewDevice(self, mockedClient, mockedCmdSet):
        """
        The constructor must create a new command set based on the device
        configuration when the isNew flag is True.
        """
        mockedClient.side_effect = self.mockedClient
        mockedCmdSet.side_effect = self.mockedCmdSet
        name = self.deviceConfig['commandSet']['model']
        emitter = self.deviceConfig['commandSet']['emitterGpio']
        receiver = self.deviceConfig['commandSet']['receiverGpio']
        description = self.deviceConfig['commandSet']['description']
        device = Device(logging, self.mockedAppConfig,      # noqa: F841
                        self.deviceConfig, isNew=True)
        self.mockedCmdSet.assert_called_once_with(name, emitter_gpio=emitter,
                                                  receiver_gpio=receiver,
                                                  description=description)

    @patch('device.Device.CommandSet.load')
    @patch('device.Device.mqtt.Client')
    def test_constructorLoadDevice(self, mockedClient, mockedCmdSetLoad):
        """
        The constructor must load an existing command set when the
        isNew flag is Flase.
        """
        mockedClient.side_effect = self.mockedClient
        manufacturer = self.deviceConfig['commandSet']['manufacturer']
        model = self.deviceConfig['commandSet']['model']
        device = Device(logging, self.mockedAppConfig,      # noqa: F841
                        self.deviceConfig)
        mockedCmdSetLoad.assert_called_once_with(f"./commandSets/"
                                                 f"{manufacturer}"
                                                 f"/{model}.json")

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    @patch('device.Device.Device._initMqttClient')
    def test_constructorInitMqttClient(self, mockedClientInit,
                                       mockedClient, mockedCmdSet):
        """
        The constructor must initialize the MQTT client with the appropriate
        broker/user information.
        """
        mockedClient.side_effect = self.mockedClient
        mockedCmdSet.side_effect = self.mockedCmdSet
        username = self.mockedAppConfig.getUserName()
        password = self.mockedAppConfig.getUserPassword()
        hostname = self.mockedAppConfig.getBrokerHostname()
        port = self.mockedAppConfig.getBrokerPort()
        device = Device(logging, self.mockedAppConfig,      # noqa: F841
                        self.deviceConfig)
        mockedClientInit.assert_called_once_with(username, password,
                                                 hostname, port)
