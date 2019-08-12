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
except:
    long_description = description

setup(
    name="astral",
    version="2.0.0a",
    description=description,
    long_description=long_description,
    author="Simon Kennedy",
    author_email="sffjunkie+code@gmail.com",
    url="https://github.com/sffjunkie/astral",
    project_urls={
        "Documentation": "https://astral.readthedocs.io/en/stable/index.html",
        "Source": "https://github.com/sffjunkie/astral",
        "Issues": "https://github.com/sffjunkie/astral/issues",
    },
    keywords="sun moon sunrise sunset dawn dusk",
    license="Apache-2.0",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
    package_dir={"": "src"},
    packages=["astral"],
    install_requires=["pytz", 'dataclasses;python_version=="3.6"'],
    tests_require=["pytest-runner"],
    zip_safe=True,
)
