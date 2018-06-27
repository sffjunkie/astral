"""Monkey patch distutils to also use setup-dev.cfg and setuptools to add README.md to the default files"""

import os
import sys
import distutils.dist
from distutils.util import (check_environ, convert_path)
from distutils.debug import DEBUG
import setuptools.command.sdist


def find_config_files(self):
    """Find as many configuration files as should be processed for this
    platform, and return a list of filenames in the order in which they
    should be parsed.  The filenames returned are guaranteed to exist
    (modulo nasty race conditions).

    There are three possible config files: distutils.cfg in the
    Distutils installation directory (ie. where the top-level
    Distutils __inst__.py file lives), a file in the user's home
    directory named .pydistutils.cfg on Unix and pydistutils.cfg
    on Windows/Mac; and setup.cfg in the current directory.

    The file in the user's home directory can be disabled with the
    --no-user-cfg option.
    """

    files = []
    check_environ()

    # Where to look for the system-wide Distutils config file
    sys_dir = os.path.dirname(sys.modules['distutils'].__file__)

    # Look for the system config file
    sys_file = os.path.join(sys_dir, "distutils.cfg")
    if os.path.isfile(sys_file):
        files.append(sys_file)

    # What to call the per-user config file
    if os.name == 'posix':
        user_filename = ".pydistutils.cfg"
    else:
        user_filename = "pydistutils.cfg"

    # And look for the user config file
    if self.want_user_cfg:
        user_file = os.path.join(os.path.expanduser('~'), user_filename)
        if os.path.isfile(user_file):
            files.append(user_file)

    # All platforms support local setup.cfg
    local_file = "setup.cfg"
    if os.path.isfile(local_file):
        files.append(local_file)

    local_dev_file = "setup-dev.cfg"
    if os.path.isfile(local_dev_file):
        files.append(local_dev_file)

    if DEBUG:
        self.announce("using config files: %s" % ', '.join(files))

    return files


def check_readme(self):
    self.READMES += ('README.md',)
    for f in self.READMES:
        if os.path.exists(f):
            return
    else:
        self.warn(
            "standard file not found: should have one of " +
            ', '.join(self.READMES)
        )


distutils.dist.Distribution.find_config_files = find_config_files
setuptools.command.sdist.sdist.check_readme = check_readme
