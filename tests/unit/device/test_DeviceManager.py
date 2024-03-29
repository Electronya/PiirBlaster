import json
import logging
from unittest import TestCase
from unittest.mock import Mock, patch, mock_open


import os
import sys
sys.path.append(os.path.abspath('./src'))

from device.Device import Device                            # noqa: E402
from device.DeviceManager import DeviceManager              # noqa: E402
from exceptions import DeviceFileAccess, DeviceNotFound, \
    DeviceExists                                            # noqa: E402


class TestDevMngr(TestCase):
    """
    DeviceManager class test cases.
    """
    def setUp(self):
        """
        Test cases setup.
        """
        with open('./tests/unit/device/devices.json') as devFiles:
            self.devicesStr = devFiles.read()
            self.devices = json.loads(self.devicesStr)

        self.mockDevs = []
        for device in self.devices:
            mockedDev = Mock(spec_set=Device)
            mockedDev.getName.return_value = device['name']
            mockedDev.getLocation.return_value = device['location']
            mockedDev.getConfig.return_value = device
            self.mockDevs.append(mockedDev)

        self.mockedCmdSetsDir = [
            ('./commandSets', ('jvc', 'samsung', 'sony', 'toshiba'), ()),
            ('./commandSets/jvc', (), ('cmdSetJVC1.json', 'cmdSetJVC2.json')),
            ('./commandSets/samsung', (), ('cmdSetSEC1.json',
                                           'cmdsetSEC2.json',
                                           'cmdSetSEC3.json')),
            ('./commandSets/sony', (), ('cmdSetSony1.json',
                                        'cmdSetSony2.json')),
            ('./commandSets/tochiba', (), ('cmdSetTosh1.json',
                                           'cmdSetTosh2.json')),
        ]

        self.mockedSecCmdsets = [('./commandSets/samsung', (),
                                 ('cmdSetSEC1.json',
                                  'cmdsetSEC2.json',
                                  'cmdSetSEC3.json'))]

        self.mockedToshCmdSets = [('./commandSets/tochiba', (),
                                  ('cmdSetTosh1.json', 'cmdSetTosh2.json'))]

    @patch('device.DeviceManager.Device')
    def test_constructorDevsFileError(self, mockedDevice):
        """
        The constructor must raise a DeviceFileAccess errror if
        access to the device configurations file failed.
        """
        mockedDevice.side_effect = self.mockDevs
        with patch('builtins.open', mock_open(read_data=self.devicesStr)) \
                as mockedFile, self.assertRaises(DeviceFileAccess) as context:
            mockedFile.side_effect = OSError
            devMngr = DeviceManager(logging, {})                # noqa: F841
            self.assertTrue('unable to access device configuraion file'
                            in str(context.exception),
                            'DeviceManager failed to raise a DeviceFileAccess '
                            'exception when access to the device '
                            'configurations access failed.')

    @patch('device.DeviceManager.Device')
    def test_constructorOpenDevsFile(self, mockedDevice):
        """
        The constructor must open the device configurations file.
        """
        mockedDevice.side_effect = self.mockDevs
        with patch('builtins.open',
                   mock_open(read_data=self.devicesStr)) as mockedFile:
            devMngr = DeviceManager(logging, {})                # noqa: F841
            mockedFile.assert_called_once_with('./config/components/'
                                               'devices.json')

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
        The startLoops method must call the startLoop method of each devices.
        """
        mockedDevice.side_effect = self.mockDevs
        with patch('builtins.open', mock_open(read_data=self.devicesStr)):
            devMngr = DeviceManager(logging, {})
            devMngr.startLoops()
            for dev in self.mockDevs:
                self.assertTrue(dev.startLoop.called,
                                'DeviceManager startLoops method failed to '
                                'call the startLoop method on all '
                                'the devices.')

    @patch('device.DeviceManager.Device')
    def test_stopLoops(self, mockedDevice):
        """
        The stopLoops method must call the stopLoop method of each devices.
        """
        mockedDevice.side_effect = self.mockDevs
        with patch('builtins.open', mock_open(read_data=self.devicesStr)):
            devMngr = DeviceManager(logging, {})
            devMngr.stopLoops()
            for dev in self.mockDevs:
                self.assertTrue(dev.stopLoop.called,
                                'DeviceManager startLoops method failed to '
                                'call the stopLoop method on all '
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
        The getDeviceByName method must raise a DeviceNotFound when the
        requested device is not found.
        """
        mockedDevice.side_effect = self.mockDevs
        lookupName = 'prout'
        lookupLocation = 'atlantic'
        with patch('builtins.open', mock_open(read_data=self.devicesStr)):
            devMngr = DeviceManager(logging, {})
            with self.assertRaises(DeviceNotFound) as context:
                devMngr.getDeviceByName(lookupName, lookupLocation)
            print(str(context.exception))
            self.assertTrue(f"device {lookupLocation}.{lookupName} not found"
                            in str(context.exception),
                            'DeviceManager getDeviceByName failed to raise '
                            'a DeviceNotFound when unable to find the device.')

    @patch('device.DeviceManager.Device')
    def test_getDeviceByNameDevFound(self, mockedDevice):
        """
        The getDeviceByName method must return the found device.
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
        The getDeviceByIdx method must raise an IndexError if the requested
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
        The getDeviceCount method must return the number of active devices.
        """
        mockedDevice.side_effect = self.mockDevs
        with patch('builtins.open', mock_open(read_data=self.devicesStr)):
            devMngr = DeviceManager(logging, {})
            devCount = devMngr.getDeviceCount()
            self.assertEqual(devCount, len(self.devices),
                             'DeviceManager getDevsCount failed to return'
                             'the number of active devices.')

    @patch('device.DeviceManager.Device')
    def test_getDevices(self, mockedDevice):
        """
        The getDevices method must return the list of active devices.
        """
        mockedDevice.side_effect = self.mockDevs
        with patch('builtins.open', mock_open(read_data=self.devicesStr)):
            devMngr = DeviceManager(logging, {})
            deviceList = devMngr.getDevices()
            self.assertEqual(len(deviceList), len(self.devices),
                             'DeviceManager getDevices failed to return the'
                             'list of active devices.')
            for device in deviceList:
                self.assertTrue(isinstance(device, Mock),
                                'DeviceManager getDevices failed to return the'
                                'list of active devices.')

    @patch('device.DeviceManager.Device')
    def test_addDeviceAlreadyExist(self, mockedDevice):
        """
        The addDevice method must raise an DeviceExist error if a device with
        the same location and name is already active.
        """
        mockedDevice.side_effect = self.mockDevs
        with patch('builtins.open', mock_open(read_data=self.devicesStr)):
            devMngr = DeviceManager(logging, {})
            with self.assertRaises(DeviceExists) as context:
                devMngr.addDevice(self.devices[0])
            self.assertTrue(f"device {self.devices[0]['location']}."
                            f"{self.devices[0]['name']}" in
                            str(context.exception),
                            'DeviceManager addDevice failed to raise a '
                            'DeviceExists exception when there already an '
                            'active device with the same name and location '
                            'than the new one.')

    @patch('device.DeviceManager.Device')
    def test_addDeviceCreateDev(self, mockedDevice):
        """
        The addDevice method must create a new Device and add it
        to the active list.
        """
        mockedDevConfig = {
            'name': 'testDev4',
            'location': 'testLocation4',
            'linkedEmitter': 'OUT0',
            'commandSet': {
                'model': 'testModel4',
                'manufacturer': 'testManufacturer4',
                'description': 'My test device 4',
                'emitterGpio': 3,
                'receiverGpio': 6,
                'packetGap': 0.04
            },
            'topicPrefix': 'testPrefix4',
            'lastWill': {
                'qos': 2,
                'retain': True
            }
        }
        mockedDev = Mock()
        mockedDev.loop_start.return_value = None
        mockedDev.loop_start.return_value = None
        self.mockDevs.append(mockedDev)
        mockedDevice.side_effect = self.mockDevs
        with patch('builtins.open', mock_open(read_data=self.devicesStr)):
            devMngr = DeviceManager(logging, {})
            devMngr.addDevice(mockedDevConfig)
            self.assertEqual(len(devMngr.devices), len(self.devices) + 1,
                             'DeviceManager addDevice failed to create the '
                             'new device and add it to the active list.')
            self.assertTrue(devMngr.devices[-1] is mockedDev,
                            'DeviceManager addDevice failed to create the '
                            'new device and add it to the active list.')

    @patch('device.DeviceManager.Device')
    def test_saveDevicesGatterDevConfigs(self, mockedDevices):
        """
        The saveDevices method must gatter the configuration of
        each active devices.
        """
        mockedDevices.side_effect = self.mockDevs
        with patch('builtins.open', mock_open(read_data=self.devicesStr)):
            devMngr = DeviceManager(logging, {})
            devMngr.saveDevices()
            for device in self.mockDevs:
                device.getConfig.assert_called_once()

    @patch('device.DeviceManager.Device')
    def test_saveDevicesDevsFileError(self, mockedDevice):
        """
        The saveDevice method must raise a DeviceFileAccess error if
        the access to the device configuration file generates errors.
        """
        mockedDevice.side_effect = self.mockDevs
        with patch('builtins.open', mock_open(read_data=self.devicesStr)):
            devMngr = DeviceManager(logging, {})

        with patch('builtins.open', mock_open(read_data=self.devicesStr)) \
                as mockedFile, self.assertRaises(DeviceFileAccess) as context:
            mockedFile.side_effect = OSError
            devMngr.saveDevices()
            self.assertTrue('unable to access device configuraion file'
                            in str(context.exception),
                            'DeviceManager saveDevices failed to raise a '
                            'DeviceFileAccess exception when the access to '
                            'the file failed.')

    @patch('device.DeviceManager.Device')
    def test_saveDevicesOpenDevsFile(self, mockedDevice):
        """
        The saveDevice method must open the device configuration file.
        """
        mockedDevice.side_effect = self.mockDevs
        with patch('builtins.open', mock_open(read_data=self.devicesStr)):
            devMngr = DeviceManager(logging, {})

        with patch('builtins.open', mock_open(read_data=self.devicesStr)) \
                as mockedFile:
            devMngr.saveDevices()
            mockedFile.assert_called_once_with('./config/components'
                                               '/devices.json')

    @patch('device.DeviceManager.Device')
    def test_saveDevicesWriteDevsConfig(self, mockedDevice):
        """
        The saveDevices must write the configuration of all the active
        Device in the device configuration file.
        """
        mockedDevConfig = {
            'name': 'testDev4',
            'location': 'testLocation4',
            'linkedEmitter': 'OUT0',
            'commandSet': {
                'model': 'testModel4',
                'manufacturer': 'testManufacturer4',
                'Description': 'My test device 4',
                'emitterGpio': 3,
                'receiverGpio': 6,
                'packetGap': 0.04
            },
            'topicPrefix': 'testPrefix4',
            'lastWill': {
                'qos': 2,
                'retain': True
            }
        }
        mockedDev = Mock()
        mockedDev.loop_start.return_value = None
        mockedDev.loop_start.return_value = None
        mockedDev.getConfig.return_value = mockedDevConfig
        self.mockDevs.append(mockedDev)
        mockedDevice.side_effect = self.mockDevs
        with patch('builtins.open', mock_open(read_data=self.devicesStr)):
            devMngr = DeviceManager(logging, {})
            devMngr.addDevice(mockedDevConfig)

        with patch('builtins.open', mock_open(read_data=self.devicesStr)) \
                as mockedFile:
            self.devices.append(mockedDevConfig)
            devMngr.saveDevices()
            mockedFile().write.assert_called_once_with(json
                                                       .dumps(self.devices,
                                                              sort_keys=True,
                                                              indent=2))

    @patch('device.DeviceManager.Device')
    def test_listManufacturerWalkCmdSetsDir(self, mockedDevice):
        """
        The listManufacturer method must walk the command sets directory
        to identify the supported manufacturer.
        """
        mockedDevice.side_effect = self.mockDevs
        with patch('builtins.open', mock_open(read_data=self.devicesStr)):
            devMngr = DeviceManager(logging, {})

        with patch('os.walk') as mockedWalk:
            devMngr.listManufacturer()
            mockedWalk.assert_called_with('./commandSets')

    @patch('device.DeviceManager.Device')
    def test_listManufacturerReturn(self, mockedDevice):
        """
        The listManufacturer method must return the list of
        supported manufacturer.
        """
        mockedDevice.side_effect = self.mockDevs
        with patch('builtins.open', mock_open(read_data=self.devicesStr)):
            devMngr = DeviceManager(logging, {})

        with patch('os.walk') as mockedWalk:
            mockedWalk.return_value = self.mockedCmdSetsDir
            resultManufacturer = devMngr.listManufacturer()
            self.assertEqual(tuple(resultManufacturer),
                             self.mockedCmdSetsDir[0][1],
                             'DeviceManager listManufacturer failed to '
                             'return the list of manufacturer.')

    @patch('device.DeviceManager.Device')
    def test_listCommandSetsWalkManufDir(self, mockedDevice):
        """
        The listCommandSets must walk the passed manufacturer subdirectory.
        """
        mockedDevice.side_effect = self.mockDevs
        with patch('builtins.open', mock_open(read_data=self.devicesStr)):
            devMngr = DeviceManager(logging, {})

        with patch('os.walk') as mockedWalk:
            devMngr.listCommandSets('sony')
            mockedWalk.assert_called_with('./commandSets/sony')

    @patch('device.DeviceManager.Device')
    def test_listCommandSetsReturn(self, mockedDevice):
        """
        The listCommandSets must return the list of command sets for a given
        manufacturer.
        """
        secCmdSets = []
        for cmdSet in self.mockedSecCmdsets[0][2]:
            secCmdSets.append(cmdSet[:-5])

        toshCmdSets = []
        for cmdSet in self.mockedToshCmdSets[0][2]:
            toshCmdSets.append(cmdSet[:-5])

        mockedDevice.side_effect = self.mockDevs
        with patch('builtins.open', mock_open(read_data=self.devicesStr)):
            devMngr = DeviceManager(logging, {})

        with patch('os.walk') as mockedWalk:
            mockedWalk.return_value = self.mockedSecCmdsets
            resultCmdSets = devMngr.listCommandSets('samsung')
            self.assertEqual(resultCmdSets, secCmdSets,
                             'DeviceManager listCommandSets failed to return '
                             'the list of command sets for a given '
                             'manufacturer.')

            mockedWalk.return_value = self.mockedToshCmdSets
            resultCmdSets = devMngr.listCommandSets('toshiba')
            self.assertEqual(resultCmdSets, toshCmdSets,
                             'DeviceManager listCommandSets failed to return '
                             'the list of command sets for a given '
                             'manufacturer.')
