# Copyright 2009-2015, Simon Kennedy, sffjunkie+code@gmail.com

import os
import sys
from setuptools import setup

PACKAGE_DIR = 'src'

sys.path.insert(0, PACKAGE_DIR)

from astral import __version__ as astral_version

def dev_dir():
    dev_home = os.environ.get('DEV_HOME', None)
    if not dev_home:
        return None

    return os.path.join(dev_home, 'projects')

cmd_class = {}
tests_require = []

dd = dev_dir()
if dd:
    sys.path.insert(0, dd)

try:
    import common.test
    cmd_class['test'] = common.test.TestCommand
    tests_require.extend(common.test.requires)
except ImportError:
    print('Unable to import test command. Skipping. Try running tool from command line e.g. tox')
    pass

#try:
#    import common.clean
#    cmd_class['clean'] = common.clean.CleanCommand
#except ImportError:
#    pass

description = 'Calculations for the position of the sun and moon.'
try:
    from common.setup_funcs import read_contents
    long_description = read_contents(os.path.dirname(__file__), 'README')
except ImportError:
    long_description = description
        
setup(name='astral',
      version=astral_version,
      description=description,
      long_description=long_description,
      author='Simon Kennedy',
      author_email='sffjunkie+code@gmail.com',
      url="https://launchpad.net/astral",
      license='Apache-2.0',
      classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
      ],
      package_dir={'': PACKAGE_DIR},
      py_modules=['astral'],
      install_requires=['pytz'],
    
      cmdclass = cmd_class,
      tests_require=tests_require,
)
