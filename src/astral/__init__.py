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
timezone, latitude, longitude and elevation. The lookups can be perfomed using the
:func:`lookup` function defined in :mod:`astral.geocoder`

For example ::

    >>> from astral.geocoder import lookup
    >>> location = lookup('London')
    >>> print('Information for %s' % location.name)
    Information for London
    >>> timezone = location.timezone
    >>> print('Timezone: %s' % timezone)
    Timezone: Europe/London
    >>> print('Latitude: %.02f; Longitude: %.02f' % (location.latitude, location.longitude))
    Latitude: 51.47; Longitude: -0.00
    >>> from datetime import date
    >>> import astral.sun
    >>> d = date(2009,4,22)
    >>> import pytz
    >>> tzinfo = pytz.timezone(timezone)
    >>> sun = astral.sun.sun(location, date=d, tzinfo=tzinfo)
    >>> print('Dawn:    %s' % str(sun['dawn']))
    Dawn:    2009-04-22 05:12:56+01:00

.. note::

   The `Astral` and `GoogleGeocoder` classes from earlier versions have been
   removed.
"""

import datetime
import re
from dataclasses import dataclass
from enum import Enum

try:
    import pytz
except ImportError:
    raise ImportError(("The astral module requires the pytz module to be available."))


__all__ = [
    "AstralError",
    "LocationInfo",
    "Observer",
    "SunDirection",
    "latlng_to_float",
    "now",
    "today",
]

__version__ = "2.0.0alpha"
__author__ = "Simon Kennedy <sffjunkie+code@gmail.com>"


def now(tzinfo: datetime.tzinfo = pytz.utc) -> datetime.datetime:
    """Returns the current time in the specified time zone"""
    return pytz.utc.localize(datetime.datetime.utcnow()).astimezone(tzinfo)


def today(tzinfo: datetime.tzinfo = pytz.utc) -> datetime.date:
    """Returns the current date in the specified time zone"""
    return now(tzinfo).date()


def latlng_to_float(dms: str) -> float:
    """Converts degrees°minutes'seconds", or a float encoded as a string, to a float"""

    _dms_re = r"(?P<deg>\d{1,3})[°](?P<min>\d{1,2})[′']((?P<sec>\d{1,2})[″\"])?(?P<dir>[NSEW])"
    m = re.match(_dms_re, dms, flags=re.IGNORECASE)
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
        return float(dms)


class AstralError(Exception):
    """Astral base exception class"""


class SunDirection(Enum):
    RISING = 1
    SETTING = -1


@dataclass
class Observer:
    """Defines the location of an observer.

    Latitude and longitude can be set either as a float or as a string. For strings they must
    be of the form

        degrees°minutes'[N|S|E|W] e.g. 51°31'N

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

    Latitude and longitude can be set either as a float or as a string. For strings they must
    be of the form

        degrees°minutes'[N|S|E|W] e.g. 51°31'N

    :param name:      Location name (can be any string)
    :param region:    Region location is in (can be any string)
    :param timezone:  The location's time zone (a list of time zone names can be obtained from
                      `pytz.all_timezones`)
    :param latitude:  Latitude - Northern latitudes should be positive
    :param longitude: Longitude - Eastern longitudes should be positive
    :param elevation: Elevation in metres above sea level.
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
