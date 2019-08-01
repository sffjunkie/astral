"""Sun calculations in a local timezone"""

import datetime
from typing import Dict, Optional, Tuple

import pytz

import astral.utc
from astral import Observer, SunDirection


def now(tzinfo: datetime.tzinfo) -> datetime.datetime:
    """Returns the current local time in a time zone"""
    return pytz.utc.localize(datetime.datetime.utcnow()).astimezone(tzinfo)


def today(tzinfo: datetime.tzinfo) -> datetime.date:
    """Returns the current local date in a time zone"""
    return now(tzinfo).date()


def solar_noon(
    observer: Observer,
    date: Optional[datetime.date] = None,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> datetime.datetime:
    """Returns the solar noon time in a local timezone

    :param observer: An observer viewing the sun at a specific, latitude, longitude and elevation
    :param date:     The date to calculate for (Default: today)
    :param tzinfo:   A tzinfo for the local time zone (Default: :class:`pytz.utc`)
    """
    t = astral.utc.solar_noon(observer, date)
    return t.astimezone(tzinfo)


def solar_midnight(
    observer: Observer,
    date: Optional[datetime.date] = None,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> datetime.datetime:
    """Returns the solar midnight time in a local timezone

    :param observer: An observer viewing the sun at a specific, latitude, longitude and elevation
    :param date:     The date to calculate for (Default: today)
    :param tzinfo:   A tzinfo for the local time zone (Default: :class:`pytz.utc`)
    """
    t = astral.utc.solar_midnight(observer, date)
    return t.astimezone(tzinfo)


def dawn(
    observer: Observer,
    date: Optional[datetime.date] = None,
    depression: float = 6.0,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> datetime.datetime:
    """Returns the dawn time in a local timezone

    :param observer:   An observer viewing the sun at a specific, latitude, longitude and elevation
    :param date:       The date to calculate for (Default: today)
    :param depression: The solar depression to use for the dawn time (Default: 6.0 degrees)
    :param tzinfo:     A tzinfo for the local time zone (Default: :class:`pytz.utc`)
    """
    return astral.utc.dawn(observer, date, depression).astimezone(tzinfo)


def sunrise(
    observer: Observer,
    date: Optional[datetime.date] = None,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> datetime.datetime:
    """Returns the sunrise time in a local timezone

    :param observer: An observer viewing the sun at a specific, latitude, longitude and elevation
    :param date:     The date to calculate for (Default: today)
    :param tzinfo:   A tzinfo for the local time zone (Default: :class:`pytz.utc`)
    """
    t = astral.utc.sunrise(observer, date)
    return t.astimezone(tzinfo)


def sunset(
    observer: Observer,
    date: Optional[datetime.date] = None,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> datetime.datetime:
    """Returns the sunset time in a local timezone

    :param observer: An observer viewing the sun at a specific, latitude, longitude and elevation
    :param date:     The date to calculate for (Default: today)
    :param tzinfo:   A tzinfo for the local time zone (Default: :class:`pytz.utc`)
    """
    t = astral.utc.sunset(observer, date)
    return t.astimezone(tzinfo)


def dusk(
    observer: Observer,
    date: Optional[datetime.date] = None,
    depression: float = 6.0,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> datetime.datetime:
    """Returns the dusk time in a local timezone

    :param observer:   An observer viewing the sun at a specific, latitude, longitude and elevation
    :param date:       The date to calculate for (Default: today)
    :param depression: The solar depression to use for the dawn time (Default: 6.0 degrees)
    :param tzinfo:     A tzinfo for the local time zone (Default: :class:`pytz.utc`)
    """
    t = astral.utc.dusk(observer, date, depression)
    return t.astimezone(tzinfo)


def daylight(
    observer: Observer,
    date: Optional[datetime.date] = None,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> Tuple[datetime.datetime, datetime.datetime]:
    """Returns the start and end times of day time in a local timezone

    :param observer: An observer viewing the sun at a specific, latitude, longitude and elevation
    :param date:     The date to calculate for (Default: today)
    :param tzinfo:   A tzinfo for the local time zone (Default: :class:`pytz.utc`)
    """
    t0, t1 = astral.utc.daylight(observer, date)
    return t0.astimezone(tzinfo), t1.astimezone(tzinfo)


def night(
    observer: Observer,
    date: Optional[datetime.date] = None,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> Tuple[datetime.datetime, datetime.datetime]:
    """Returns the start and end times of night time in a local timezone

    :param observer: An observer viewing the sun at a specific, latitude, longitude and elevation
    :param date:     The date to calculate for (Default: today)
    :param tzinfo:   A tzinfo for the local time zone (Default: :class:`pytz.utc`)
    """
    t0, t1 = astral.utc.night(observer, date)
    return t0.astimezone(tzinfo), t1.astimezone(tzinfo)


def time_at_altitude(
    observer: Observer,
    altitude: float,
    date: datetime.date = None,
    direction: SunDirection = SunDirection.RISING,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> datetime.datetime:
    """Returns the time when the sun is at the specified altitude in a local timezone

    :param observer:  An observer viewing the sun at a specific, latitude, longitude and elevation
    :param altitude:  The altitude of the sun to calculate the time for
    :param date:      The date to calculate for (Default: today)
    :param direction: Whether the time is for the sun rising or setting (Default: rising)
    :param tzinfo:    A tzinfo for the local time zone (Default: :class:`pytz.utc`)
    """
    t = astral.utc.time_at_altitude(observer, altitude, date, direction)
    return t.astimezone(tzinfo)


def twilight(
    observer: Observer,
    date: Optional[datetime.date] = None,
    direction: SunDirection = SunDirection.RISING,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> Tuple[datetime.datetime, datetime.datetime]:
    """Returns the start and end times of twilight in a local timezone

    :param observer:  An observer viewing the sun at a specific, latitude, longitude and elevation
    :param date:      The date to calculate for (Default: today)
    :param direction: Whether the time is for the sun rising or setting (Default: rising)
    :param tzinfo:    A tzinfo for the local time zone (Default: :class:`pytz.utc`)
    """
    t0, t1 = astral.utc.twilight(observer, date, direction)
    return t0.astimezone(tzinfo), t1.astimezone(tzinfo)


def golden_hour(
    observer: Observer,
    date: Optional[datetime.date] = None,
    direction: SunDirection = SunDirection.RISING,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> Tuple[datetime.datetime, datetime.datetime]:
    """Returns the start and end times of the golden hour in a local timezone

    :param observer:  An observer viewing the sun at a specific, latitude, longitude and elevation
    :param date:      The date to calculate for (Default: today)
    :param direction: Whether the time is for the sun rising or setting (Default: rising)
    :param tzinfo:    A tzinfo for the local time zone (Default: :class:`pytz.utc`)
    """
    t0, t1 = astral.utc.golden_hour(observer, date, direction)
    return t0.astimezone(tzinfo), t1.astimezone(tzinfo)


def blue_hour(
    observer: Observer,
    date: Optional[datetime.date] = None,
    direction: SunDirection = SunDirection.RISING,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> Tuple[datetime.datetime, datetime.datetime]:
    """Returns the start and end times of the blue hour in a local timezone

    :param observer:  An observer viewing the sun at a specific, latitude, longitude and elevation
    :param date:      The date to calculate for (Default: today)
    :para: direction: Whether the time is for the sun rising or setting (Default: rising)
    :param tzinfo:    A tzinfo for the local time zone (Default: :class:`pytz.utc`)
    """
    t0, t1 = astral.utc.blue_hour(observer, date, direction)
    return t0.astimezone(tzinfo), t1.astimezone(tzinfo)


def rahukaalam(
    observer: Observer,
    date: Optional[datetime.date] = None,
    daytime: bool = True,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> Tuple[datetime.datetime, datetime.datetime]:
    """Returns the start and end times of Rahu Kaalam in a local timezone

    :param observer:  An observer viewing the sun at a specific, latitude, longitude and elevation
    :param date:      The date to calculate for (Default: today)
    :para: daytime:   Whether the time is during the day time or the night time (Default: True)
    :param tzinfo:    A tzinfo for the local time zone (Default: :class:`pytz.utc`)
    """
    t0, t1 = astral.utc.rahukaalam(observer, date, daytime)
    return t0.astimezone(tzinfo), t1.astimezone(tzinfo)


def sun(
    observer: Observer,
    date: Optional[datetime.date] = None,
    dawn_dusk_depression: float = 6.0,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> Dict:
    """Calculate all the info for the sun at once in a local timezone.

    :param observer:             The Observer for which to calculate the times of the sun
    :param date:                 Date to calculate for.
    :param dawn_dusk_depression: The depression to use to calculate dawn and dusk
    :returns:                    Dictionary with keys ``dawn``, ``sunrise``, ``noon``,
                                 ``sunset`` and ``dusk`` whose values are the results of
                                 the corresponding methods.
    """
    s = astral.utc.sun(observer, date, dawn_dusk_depression)
    return {key: s[key].astimezone(tzinfo) for key in s}
