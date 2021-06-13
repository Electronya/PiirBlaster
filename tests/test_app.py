from unittest import TestCase
from unittest.mock import patch

import os
import sys
sys.path.append(os.path.abspath('./src'))

from app import App                     # noqa: E402


class TestApp(TestCase):
    """
    The App class test cases.
    """
    @patch('config.Config.__init__', autospec=True)
    @patch('device.DeviceManager.__init__', autospec=True)
    def test_conctructorLoadConfig(self, configCont, devMngrConst):
        """
        The constructor must load the configuration by creating a new
        instance of the Config object.
        """
        configCont.return_value = None
        devMngrConst.return_value = None
        app = App()                                         # noqa: F841
        self.assertTrue(configCont.called,
                        'App constructor failed to load the config.')

    @patch('config.Config.__init__', autospec=True)
    @patch('device.DeviceManager.__init__', autospec=True)
    def test_constructorLoadDevMngr(self, configConst, devMngrConst):
        """
        The contructor must load the active devices by instanciating a new
        instance of the DeviceManager.
        """
        configConst.return_value = None
        devMngrConst.return_value = None
        app = App()                                         # noqa: F841
        self.assertTrue(devMngrConst.called,
                        'App constructor failed to load the devices.')

    @patch('config.Config.__init__', autospec=True)
    @patch('device.DeviceManager.__init__', autospec=True)
    @patch('device.DeviceManager.startLoops', autospec=True)
    def test_runStartDeviceLoops(self, configConst, devMngrConst,
                                 devMngrStartLoops):
        """
        The App run method must start the nertwork loop of the active
        devices by calling the device manager startLoops method.
        """
        configConst.return_value = None
        devMngrConst.return_value = None
        devMngrStartLoops.return_value = None
        app = App()
        app.run()
        self.assertTrue(devMngrStartLoops.called,
                        'App.run failed to start the loop of the devices')

    @patch('config.Config.__init__', autospec=True)
    @patch('device.DeviceManager.__init__', autospec=True)
    @patch('device.DeviceManager.stopLoops', autospec=True)
    def test_stopStopDeviceLoops(self, configConst, devMngrConst,
                                 devMngrStopLoops):
        """
        The App stop method must stop the nertwork loop of the active
        devices by calling the device manager stopLoops method.
        """
        configConst.return_value = None
        devMngrConst.return_value = None
        devMngrStopLoops.return_value = None
        app = App()
        app.stop()
        self.assertTrue(devMngrStopLoops.called,
                        'App.run failed to start the loop of the devices')
