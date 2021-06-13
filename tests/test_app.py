from unittest import TestCase
from unittest.mock import Mock, patch

import os
import sys
sys.path.append(os.path.abspath('./src'))

from app import App                     # noqa: E402
from config import Config               # noqa: 402
from device import DeviceManager        # noqa: 402


class TestApp(TestCase):
    """
    The App class test cases.
    """
    @patch('config.Config.__init__', autospec=True)
    def test_conctructorLoadConfig(self, mockedConfigConst):
        """
        The constructor must load the configuration by creating a new
        instance of the Config object.
        """
        mockedConfigConst.return_value = None
        with patch.object(DeviceManager, '__init__', lambda x, y, z: None):
            app = App()                                         # noqa: F841
            self.assertTrue(mockedConfigConst.called)
