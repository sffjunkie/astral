# Copyright 2009-2011, Simon Kennedy, code@sffjunkie.co.uk
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from distutils.core import setup

setup(name='astral',
    version='0.6.1',
    description='Calculations for the position of the sun and moon.',
    long_description="""Sun calculations for dawn, sunrise, solar noon,
    sunset, dusk, solar elevation, solar azimuth and rahukaalam.
    Moon calculation for phase.
    """,
    author='Simon Kennedy',
    author_email='code@sffjunkie.co.uk',
    url="http://www.sffjunkie.co.uk/python-astral.html",
    license='Apache-2.0',
    package_dir={'': 'astral'},
    py_modules=['astral'],
    requires=['pytz'],
)
