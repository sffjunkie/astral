# Copyright 2009-2019, Simon Kennedy, sffjunkie+code@gmail.com

import io
import os
from setuptools import setup

import monkeypatch  # noqa: F401


def read_contents(*names, **kwargs):
    return io.open(os.path.join(*names), encoding=kwargs.get("encoding", "utf8")).read()


description = "Calculations for the position of the sun and moon."
try:
    long_description = read_contents(os.path.dirname(__file__), "README.rst")
except:  # noqa
    long_description = description

setup(long_description=long_description)
