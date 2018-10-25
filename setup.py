# Copyright 2009-2018, Simon Kennedy, sffjunkie+code@gmail.com

import io
import os
from setuptools import setup

import monkeypatch # pylint: disable=W0611

def read_contents(*names, **kwargs):
    return io.open(
        os.path.join(*names),
        encoding=kwargs.get("encoding", "utf8")
    ).read()

description = 'Calculations for the position of the sun and moon.'
try:
    long_description = read_contents(os.path.dirname(__file__), 'README.rst')
except:
    long_description = description

setup(name='astral',
      version='1.7.1',
      description=description,
      long_description=long_description,
      author='Simon Kennedy',
      author_email='sffjunkie+code@gmail.com',
      url="https://github.com/sffjunkie/astral",
      project_urls={
          'Documentation': 'https://astral.readthedocs.io/en/stable/index.html',
          'Source': 'https://github.com/sffjunkie/astral',
          'Issues': 'https://github.com/sffjunkie/astral/issues',
      },
      license='Apache-2.0',
      classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
      ],
      package_dir={'': 'src'},
      py_modules=['astral'],
      install_requires=['pytz'],
      extras_require={'GoogleGeocoder': ['requests']},
      tests_require=['pytest-runner'],
)
