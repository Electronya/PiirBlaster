import json
import logging
from unittest import TestCase
from unittest import mock
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

        self.mockDevs = []
        for device in self.devices:
            mockedDev = Mock()
            mockedDev.loop_start.return_value = None
            mockedDev.loop_start.return_value = None
            mockedDev.getConfig.return_value = device
            self.mockDevs.append(mockedDev)

    @patch('device.DeviceManager.Device')
    def test_constructorOpenDevsFile(self, mockedDevice):
        """
        The constructor must open the device configurations file.
        """
        mockedDevice.side_effect = self.mockDevs
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
        mockedDevice.side_effect = self.mockDevs
        with patch('builtins.open', mock_open(read_data=self.devicesStr)):
            devMngr = DeviceManager(logging, {})         # noqa: F841
            self.assertEqual(mockedDevice.call_count, len(self.devices),
                             'DeviceManager constructor failed to create '
                             'all the device from the devices faile.')

    @patch('device.DeviceManager.Device')
    def test_startLoops(self, mockedDevice):
        """
        The startLoops method must call the loopt_start method of each devices.
        """
        mockedDevice.side_effect = self.mockDevs
        with patch('builtins.open', mock_open(read_data=self.devicesStr)):
            devMngr = DeviceManager(logging, {})
            devMngr.startLoops()
            for dev in self.mockDevs:
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
        mockedDevice.side_effect = self.mockDevs
        with patch('builtins.open', mock_open(read_data=self.devicesStr)):
            devMngr = DeviceManager(logging, {})
            defConfig = devMngr.getDefaultConfig()
            self.assertFalse(defConfig is devMngr.DEFAULT_CONFIG,
                             'DeviceManger getDefaultConfig failed to'
                             'to copy the device default config.')
            self.assertTrue(defConfig == devMngr.DEFAULT_CONFIG,
                            'DeviceManager getDefaultConfig failed to'
                            'make a copy of the device default config.')

    @patch('device.DeviceManager.Device')
    def test_getDeviceByNameNotFound(self, mockedDevice):
        """
        The getDeviceByName must raise a LookupError when the requested
        device is not found.
        """
        mockedDevice.side_effect = self.mockDevs
        with patch('builtins.open', mock_open(read_data=self.devicesStr)):
            devMngr = DeviceManager(logging, {})
            with self.assertRaises(LookupError) as context:
                devMngr.getDeviceByName('prout', 'atlantic')
            self.assertTrue('unable to find device atlantic.prout'
                            in str(context.exception),
                            'DeviceManager getDeviceByName failed to raise'
                            'a LookupError when unable to find the device.')

    @patch('device.DeviceManager.Device')
    def test_getDeviceByNameDevFound(self, mockedDevice):
        """
        The getDeviceByName must return the found device.
        """
        mockedDevice.side_effect = self.mockDevs
        with patch('builtins.open', mock_open(read_data=self.devicesStr)):
            devMngr = DeviceManager(logging, {})
            foundDev = devMngr.getDeviceByName(self.devices[1]['name'],
                                               self.devices[1]['location'])
            self.assertTrue(foundDev is self.mockDevs[1],
                            'DeviceManager getDeviceByName failed to found'
                            'the correct device.')

    @patch('device.DeviceManager.Device')
    def test_getDeviceByIdxOutRange(self, mockedDevice):
        """
        The getDeviceByIdx must raise an IndexError if the requested
        index is out of the range of the devices list.
        """
        mockedDevice.side_effect = self.mockDevs
        with patch('builtins.open', mock_open(read_data=self.devicesStr)):
            devMngr = DeviceManager(logging, {})
            with self.assertRaises(IndexError) as context:
                devMngr.getDeviceByIdx(len(self.devices) + 3)
            self.assertTrue('list index out of range'
                            in str(context.exception),
                            'DeviceManager getDeviceByIdx failed to'
                            'raise an IndexError when the requested'
                            'index is out of the range of the devices list.')
            with self.assertRaises(IndexError) as context:
                devMngr.getDeviceByIdx((len(self.devices) + 3) * -1)
            self.assertTrue('list index out of range'
                            in str(context.exception),
                            'DeviceManager getDeviceByIdx failed to'
                            'raise an IndexError when the requested'
                            'index is out of the range of the devices list.')

    @patch('device.DeviceManager.Device')
    def test_getDeviceCount(self, mockedDevice):
        """
        The getDeviceCount must return the number of active devices.
        """
        mockedDevice.side_effect = self.mockDevs
        with patch('builtins.open', mock_open(read_data=self.devicesStr)):
            devMngr = DeviceManager(logging, {})
            devCount = devMngr.getDeviceCount()
            self.assertEqual(devCount, len(self.devices),
                             'DeviceManager getDevsCount failed to return'
                             'the number of active devices.')
