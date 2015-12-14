# Copyright 2009-2015, Simon Kennedy, sffjunkie+code@gmail.com

import io
import os
import sys
from setuptools import setup

cmd_class = {}
tests_require = []
try:
    dev_home = os.environ['DEV_HOME']
    common = os.path.join(dev_home, 'projects', 'build-common')
    sys.path.insert(0, common)

    from tox import ToxCommand
    cmd_class['test'] = ToxCommand
    tests_require.append['tox']
    print(tox)

    #from clean import CleanCommand
    #cmd_class['clean'] = CleanCommand
except:
    pass


def read(*names, **kwargs):
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ).read()

        
setup(name='astral',
      version='0.8.2',
      description='Calculations for the position of the sun and moon.',
      long_description=read('README'),
      author='Simon Kennedy',
      author_email='sffjunkie+code@gmail.com',
      url="https://launchpad.net/astral",
      license='Apache-2.0',
      package_dir={'': 'src'},
      py_modules=['astral'],
      install_requires=['pytz'],
      classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
      ],
    
      cmdclass = cmd_class,
      tests_require=tests_require,
)
