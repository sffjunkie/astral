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

The :mod:`astral` package provides the means to calculate the following times of the sun

* dawn
* sunrise
* noon
* midnight
* sunset
* dusk
* daylight
* night
* twilight
* blue hour
* golden hour
* rahukaalam

plus solar azimuth and elevation at a specific latitude/longitude.
It can also calculate the moon phase for a specific date.

The package also provides a self contained geocoder to turn a small set of
location names into timezone, latitude and longitude. The lookups
can be perfomed using the :func:`~astral.geocoder.lookup` function defined in
:mod:`astral.geocoder`

.. note::

   The `Astral` and `GoogleGeocoder` classes from earlier versions have been
   removed.
"""

import datetime
import re
from dataclasses import dataclass
from enum import Enum
from math import fabs
from typing import Any, Union

try:
    import pytz
except ImportError:
    raise ImportError(("The astral module requires the pytz module to be available."))


__all__ = [
    "Depression",
    "SunDirection",
    "Observer",
    "LocationInfo",
    "now",
    "today",
    "dms_to_float",
]

__version__ = "2.0-alpha"
__author__ = "Simon Kennedy <sffjunkie+code@gmail.com>"


def now(tzinfo: datetime.tzinfo = pytz.utc) -> datetime.datetime:
    """Returns the current time in the specified time zone"""
    return pytz.utc.localize(datetime.datetime.utcnow()).astimezone(tzinfo)


def today(tzinfo: datetime.tzinfo = pytz.utc) -> datetime.date:
    """Returns the current date in the specified time zone"""
    return now(tzinfo).date()


def dms_to_float(dms: Union[str, float], limit: float) -> float:
    """Converts as string of the form `degrees°minutes'seconds"[N|S|E|W]`,
    or a float encoded as a string, to a float

    N and E return positive values
    S and W return negative values

    Args:
        dms: string to convert

    Returns:
        The number of degrees as a float
    """

    try:
        res = float(dms)
    except ValueError:
        _dms_re = r"(?P<deg>\-?\d{1,3})[°]((?P<min>\d{1,2})[′'])?((?P<sec>\d{1,2})[″\"])?(?P<dir>[NSEW])?"
        m = re.match(_dms_re, str(dms), flags=re.IGNORECASE)
        if m:
            deg = m.group("deg")
            min_ = m.group("min")
            sec = m.group("sec")
            dir_ = m.group("dir")

            res = float(deg)
            if min_:
                res += float(min_) / 60
            if sec:
                res += float(sec) / 3600

            if dir_ == "S" or dir_ == "W":
                res = -res
        else:
            raise ValueError("Unable to convert degrees/minutes/seconds to float")

    if fabs(res) > limit:
        raise ValueError(f"Value outside limits of +/-{limit}")

    return res


class SunDirection(Enum):
    RISING = 1
    SETTING = -1


@dataclass
class Observer:
    """Defines the location of an observer on Earth.

    Latitude and longitude can be set either as a float or as a string. For strings they must
    be of the form

        degrees°minutes'seconds"[N|S|E|W] e.g. 51°31'N

    `minutes’` & `seconds”` are optional.

    Args:
        latitude:   Latitude - Northern latitudes should be positive
        longitude:  Longitude - Eastern longitudes should be positive
        elevation:  Elevation in metres above sea level.
    """

    latitude: float = 51.4733
    longitude: float = -0.00088
    elevation: float = 24.0

    def __setattr__(self, name: str, value: Union[float, str]):
        if name == "latitude":
            value = dms_to_float(value, 90.0)
        elif name == "longitude":
            value = dms_to_float(value, 180.0)
        elif name == "elevation":
            value = float(value)
        super(Observer, self).__setattr__(name, value)


# Note: we don't derive from Observer because dataclasses add fields of Observer
# before LocationInfo's which puts the arguments in the wrong order for us.
@dataclass
class LocationInfo:
    """Defines a location on Earth.

    Latitude and longitude can be set either as a float or as a string. For strings they must
    be of the form

        degrees°minutes'seconds"[N|S|E|W] e.g. 51°31'N

    `minutes’` & `seconds”` are optional.

    Note:
        functions which are defined to take an Observer can also be passed a LocationInfo
        instance.

    Args:
        name:      Location name (can be any string)
        region:    Region location is in (can be any string)
        timezone:  The location's time zone (a list of time zone names can be obtained from
                      `pytz.all_timezones`)
        latitude:  Latitude - Northern latitudes should be positive
        longitude: Longitude - Eastern longitudes should be positive
        elevation: Elevation in metres above sea level.
    """

    name: str = "Greenwich"
    region: str = "England"
    timezone: str = "Europe/London"
    latitude: float = 51.4733
    longitude: float = -0.00088
    elevation: float = 24.0

    def __setattr__(self, name: str, value: Union[float, str]):
        if name == "latitude":
            value = dms_to_float(value, 90.0)
        elif name == "longitude":
            value = dms_to_float(value, 180.0)
        elif name == "elevation":
            value = float(value)
        super(LocationInfo, self).__setattr__(name, value)

    @property
    def timezone_group(self):
        return self.timezone.split("/")[0]
