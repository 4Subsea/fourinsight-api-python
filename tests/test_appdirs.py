import os
from unittest.mock import patch

from fourinsight.api import appdirs

@patch("fourinsight.api.appdirs.system")
class Test_user_data_dir:

    def test_no_module_name(self, mock_system):
        # Mock MacOS
        appdirs.system = "darwin"
        path = appdirs.user_data_dir()
        assert path == os.path.normpath(os.path.expanduser("~/.config/.fourinsight"))

        # Mock Windows
        appdirs.system = "win32"
        path = appdirs.user_data_dir()
        assert path == os.path.normpath(os.path.expanduser("~/.fourinsight"))

        # Mock UNIX / other
        appdirs.system = "linux"
        path = appdirs.user_data_dir()
        assert path == os.path.normpath(os.path.expanduser("~/.fourinsight"))

    def test_module_name(self, mock_system):
        # Mock MacOS
        appdirs.system = "darwin"
        path = appdirs.user_data_dir("api")
        assert path == os.path.normpath(os.path.expanduser("~/.config/.fourinsight/api"))

        # Mock Windows
        appdirs.system = "win32"
        path = appdirs.user_data_dir("api")
        assert path == os.path.normpath(os.path.expanduser("~/.fourinsight/api"))

        # Mock UNIX / other
        appdirs.system = "linux"
        path = appdirs.user_data_dir("api")
        assert path == os.path.normpath(os.path.expanduser("~/.fourinsight/api"))
