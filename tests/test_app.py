from unittest import TestCase
from unittest.mock import Mock, patch

import os
import sys
sys.path.append(os.path.abspath('./src'))

from app import App                     # noqa: E402


class TestApp(TestCase):
    """
    The App class test cases.
    """
    @patch('app.Config')
    @patch('app.DeviceManager')
    def test_conctructorLoadConfig(self, mockedConfig, mockedDevMngr):
        """
        The constructor must load the configuration by creating a new
        instance of the Config object.
        """
        app = App()                                         # noqa: F841
        self.assertTrue(mockedConfig.called,
                        'App constructor failed to load the config.')

    @patch('app.Config')
    @patch('app.DeviceManager')
    def test_constructorLoadDevMngr(self, mockedConfig, mockedDevMngr):
        """
        The contructor must load the active devices by instanciating a new
        instance of the DeviceManager.
        """
        app = App()                                         # noqa: F841
        self.assertTrue(mockedDevMngr.called,
                        'App constructor failed to load the devices.')

    @patch('app.Config')
    @patch('app.DeviceManager')
    def test_runStartDeviceLoops(self, mockedConfig, mockedDevMngr):
        """
        The App run method must start the nertwork loop of the active
        devices by calling the device manager startLoops method.
        """
        devMngrMock = Mock()
        devMngrMock.startLoops.return_value = None
        app = App()
        app.deviceMngr = devMngrMock
        app.run()
        self.assertTrue(devMngrMock.startLoops.called,
                        'App.run failed to start the loop of the devices')

    @patch('app.Config')
    @patch('app.DeviceManager')
    def test_stopStopDeviceLoops(self, mockedConfig, mockedDevMngr):
        """
        The App stop method must stop the nertwork loop of the active
        devices by calling the device manager stopLoops method.
        """
        devMngrMock = Mock()
        devMngrMock.stopLoops.return_value = None
        app = App()
        app.deviceMngr = devMngrMock
        app.stop()
        self.assertTrue(devMngrMock.stopLoops.called,
                        'App.run failed to start the loop of the devices')
