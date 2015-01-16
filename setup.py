# Copyright 2009-2014, Simon Kennedy, sffjunkie+code@gmail.com

import io
import sys
import os.path
from setuptools import setup
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
        
    def run_tests(self):
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)

def read(*names, **kwargs):
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ).read()

        
setup(name='astral',
      version='0.7.5',
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
    
      tests_require=['tox'],
      cmdclass = {'test': Tox},
)
