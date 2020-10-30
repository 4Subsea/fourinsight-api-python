"""
This code was taken from https://github.com/ActiveState/appdirs (v1.4.4) and
modified to suit our purposes.
"""
import os
import sys

if sys.platform.startswith("java"):  # pragma: no cover
    import platform

    os_name = platform.java_ver()[3][0]
    if os_name.startswith("Windows"):
        system = "win32"
    elif os_name.startswith("Mac"):
        system = "darwin"
    else:
        system = "linux2"
else:
    system = sys.platform


def user_data_dir(module_name=None):
    """
    Return full path to the user-specific data dir for a ``fourinsight``
    submodule. "module_name" is the name of the different submodules. If None,
    just the ``fourinsight`` root directory is returned.

    OS specific directories are:
        Mac OS X:               ~/.config/.fourinsight/<module_name>
        Unix:                   ~/.fourinsight/<module_name>
        Windows:                ~/.fourinsight/<module_name>

    """
    if system == "darwin":
        path = os.path.expanduser("~/.config/.fourinsight")
    else:
        path = os.path.expanduser("~/.fourinsight")

    if module_name:
        path = os.path.join(path, module_name)
    return os.path.normpath(path)
