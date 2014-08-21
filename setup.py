# Copyright 2009-2014, Simon Kennedy, sffjunkie+code@gmail.com

from setuptools import setup

setup(name='astral',
    version='0.7.4',
    description='Calculations for the position of the sun and moon.',
    long_description="""Sun calculations for dawn, sunrise, solar noon,
    sunset, dusk, solar elevation, solar azimuth and rahukaalam.
    Moon calculation for phase.
    """,
    author='Simon Kennedy',
    author_email='sffjunkie+code@gmail.com',
    url="http://www.sffjunkie.co.uk/python-astral.html",
    license='Apache-2.0',
    package_dir={'': 'src'},
    py_modules=['astral'],
    install_requires=['pytz'],
)
