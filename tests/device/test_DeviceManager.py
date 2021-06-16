import json
import logging
from unittest import TestCase
from unittest.mock import Mock, patch, mock_open


import os
import sys
sys.path.append(os.path.abspath('./src'))

from device.DeviceManager import DeviceManager              # noqa: E402


class TestDevMngr(TestCase):
    """
    DeviceManager class test cases.
    """
    def setUp(self):
        """
        Test cases setup.
        """
        with open('./tests/device/devices.json') as devFiles:
            self.devicesStr = devFiles.read()
            self.devices = json.loads(self.devicesStr)

    @patch('device.DeviceManager.Device')
    def test_constructorOpenDevsFile(self, mockedDevice):
        """
        The constructor must open the device configurations file.
        """
        devs = []
        for device in self.devices:
            mockedDev = Mock()
            devs.append(mockedDev)
        mockedDevice.side_effect = devs
        with patch('builtins.open',
                   mock_open(read_data=self.devicesStr)) as mockedFile:
            devMngr = DeviceManager(logging, {})                # noqa: F841
            mockedFile.assert_called_with('./config/components/devices.json')

    @patch('device.DeviceManager.Device')
    def test_constructorCreateDevs(self, mockedDevice):
        """
        The constructor must create all the device in the from
        the devices file.
        """
        devs = []
        for device in self.devices:
            mockedDev = Mock()
            devs.append(mockedDev)
        mockedDevice.side_effect = devs
        with patch('builtins.open', mock_open(read_data=self.devicesStr)):
            appConfig = {}
            devMngr = DeviceManager(logging, appConfig)         # noqa: F841
            self.assertEqual(mockedDevice.call_count, len(self.devices),
                             'DeviceManager constructor failed to create '
                             'all the device from the devices faile.')

    @patch('device.DeviceManager.Device')
    def test_startLoops(self, mockedDevice):
        """
        The startLoops method must call the loopt_start method of each devices.
        """
        devs = []
        for device in self.devices:
            mockedDev = Mock()
            mockedDev.loop_start.return_value = None
            devs.append(mockedDev)
        mockedDevice.side_effect = devs
        with patch('builtins.open', mock_open(read_data=self.devicesStr)):
            appConfig = {}
            devMngr = DeviceManager(logging, appConfig)
            devMngr.startLoops()
            for dev in devs:
                self.assertTrue(dev.loop_start.called,
                                'DeviceManager startLoops method failed to '
                                'call the loop_start method on all '
                                'the devices.')

    @patch('device.DeviceManager.Device')
    def test_getDefaultConfig(self, mockedDevice):
        """
        The getDefaultConfig method must return a copy of the
        device default config.
        """
        devs = []
        for device in self.devices:
            mockedDev = Mock()
            mockedDev.loop_start.return_value = None
            devs.append(mockedDev)
        mockedDevice.side_effect = devs
        with patch('builtins.open', mock_open(read_data=self.devicesStr)):
            appConfig = {}
            devMngr = DeviceManager(logging, appConfig)
            defConfig = devMngr.getDefaultConfig()
            self.assertFalse(defConfig is devMngr.DEFAULT_CONFIG,
                             'DeviceManger getDefaultConfig failed to'
                             'to copy the device default config.')
            self.assertTrue(defConfig == devMngr.DEFAULT_CONFIG,
                            'DeviceManager getDefaultConfig failed to'
                            'make a copy of the device default config.')
