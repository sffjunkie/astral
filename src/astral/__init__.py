# -*- coding: utf-8 -*-

# Copyright 2009-2019, Simon Kennedy, sffjunkie+code@gmail.com

#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""Calculations for the position of the sun and moon.

The :mod:`astral` package provides the means to calculate dawn, sunrise,
solar noon, sunset, dusk and rahukaalam times, plus solar azimuth and
elevation, for specific locations or at a specific latitude/longitude. It can
also calculate the moon phase for a specific date.

The package also provides a self contained geocoder to turn location names into
timezone, latitude, longitude and elevation.

:class:`Location`
    Holds information about a location and provides functions to calculate
    the event times in its time zone.

For example ::

    >>> from astral.geocoder import lookup
    >>> location = lookup('London')
    >>> print('Information for %s' % location.name)
    Information for London
    >>> timezone = location.timezone
    >>> print('Timezone: %s' % timezone)
    Timezone: Europe/London
    >>> print('Latitude: %.02f; Longitude: %.02f' % (location.latitude, location.longitude))
    Latitude: 51.60; Longitude: 0.05
    >>> from datetime import date
    >>> import astral.local
    >>> d = date(2009,4,22)
    >>> sun = astral.local.sun(local=True, date=d)
    >>> print('Dawn:    %s' % str(sun['dawn']))
    Dawn:    2009-04-22 05:12:56+01:00

Geocoding lookups can be perfomed using the :func:`lookup` function defined in
:mod:`astral.geocoder`

.. note::

   The Astral and GoogleGeocoder classes from earlier versions have been
   removed.
"""

import re
from dataclasses import dataclass
from enum import Enum

try:
    import pytz
except ImportError:
    raise ImportError(("The astral module requires the pytz module to be available."))


__all__ = ["AstralError", "LocationInfo", "Observer", "SunDirection", "latlng_to_float"]

__version__ = "2.0.0alpha"
__author__ = "Simon Kennedy <sffjunkie+code@gmail.com>"


def latlng_to_float(dms: str) -> float:
    """Converts degrees°minutes'seconds", or a float encoded as a string, to a float"""

    _dms_re = r"(?P<deg>\d{1,3})[°](?P<min>\d{1,2})[′']((?P<sec>\d{1,2})[″\"])?(?P<dir>[NSEW])"
    m = re.match(_dms_re, dms)
    if m:
        deg = m.group("deg")
        min_ = m.group("min")
        sec = m.group("sec")
        dir_ = m.group("dir")

        res = float(deg) + (float(min_) / 60)
        if sec:
            res += float(sec) / 3600

        if dir_ == "S" or dir_ == "W":
            res = -res

        return res
    else:
        try:
            return float(dms)
        except ValueError:
            return 0


class AstralError(Exception):
    """Astral base exception class"""


class SunDirection(Enum):
    RISING = 1
    SETTING = -1


@dataclass
class Observer:
    """Defines the location of an observer.

    :param latitude:   Latitude - Northern latitudes should be positive
    :param longitude:  Longitude - Eastern longitudes should be positive
    :param elevation:  Elevation in metres above sea level.
    """

    latitude: float = 51.4733
    longitude: float = -0.00088
    elevation: float = 24.0

    def __post_init__(self):
        if isinstance(self.latitude, str):
            object.__setattr__(self, "latitude", latlng_to_float(self.latitude))
        if isinstance(self.longitude, str):
            object.__setattr__(self, "longitude", latlng_to_float(self.longitude))
        object.__setattr__(self, "elevation", float(self.elevation))


# Note: we are unable to derive from Observer due to dataclasses adding add fields of Observer
# before LocationInfo's
@dataclass
class LocationInfo:
    """Defines a location on Earth.

    :param name: Location name (can be any string)
    :param region: Region location is in (can be any string)
    :param timezone: The location's time zone (a list of time zone names can be obtained from
                     `pytz.all_timezones`)
    :param latitude: Location's latitude
    :param longitude: Location's longitude
    :param elevation: The elevation in metres above sea level.
    """

    name: str = "Greenwich"
    region: str = "England"
    timezone: str = "Europe/London"
    latitude: float = 51.4733
    longitude: float = -0.00088
    elevation: float = 24.0

    def __post_init__(self):
        if isinstance(self.latitude, str):
            object.__setattr__(self, "latitude", latlng_to_float(self.latitude))
        if isinstance(self.longitude, str):
            object.__setattr__(self, "longitude", latlng_to_float(self.longitude))
        object.__setattr__(self, "elevation", float(self.elevation))

    @property
    def timezone_group(self):
        return self.timezone.split("/")[0]
