from unittest import TestCase
# from unittest.mock import Mock, patch

import os
import sys
sys.path.append(os.path.abspath('./src'))

from app import App     # noqa: 402


class TestApp(TestCase):
    """
    The App class test cases.
    """
    def test_conctructor(self):
        """
        Test the constructor.
        """
        self.assertTrue(True, 'prout.')
