"""Sun claculations in a specified local timezone"""

import datetime
from typing import Dict, Optional, Tuple

import pytz

import astral.utc
from astral import Observer, SunDirection


def now(tzinfo: datetime.tzinfo) -> datetime.datetime:
    return pytz.utc.localize(datetime.datetime.utcnow()).astimezone(tzinfo)


def today(tzinfo: datetime.tzinfo) -> datetime.date:
    return now(tzinfo).date()


def solar_noon(
    tzinfo: datetime.tzinfo, observer: Observer, date: Optional[datetime.date] = None
) -> datetime.datetime:
    t = astral.utc.solar_noon(observer, date)
    return t.astimezone(tzinfo)


def solar_midnight(
    tzinfo: datetime.tzinfo, observer: Observer, date: Optional[datetime.date] = None
) -> datetime.datetime:
    t = astral.utc.solar_midnight(observer, date)
    return t.astimezone(tzinfo)


def dawn(
    tzinfo: datetime.tzinfo,
    observer: Observer,
    date: Optional[datetime.date] = None,
    depression: float = 6.0,
) -> datetime.datetime:
    return astral.utc.dawn(observer, date, depression).astimezone(tzinfo)


def sunrise(
    tzinfo: datetime.tzinfo, observer: Observer, date: Optional[datetime.date] = None
) -> datetime.datetime:
    t = astral.utc.sunrise(observer, date)
    return t.astimezone(tzinfo)


def sunset(
    tzinfo: datetime.tzinfo, observer: Observer, date: Optional[datetime.date] = None
) -> datetime.datetime:
    t = astral.utc.sunset(observer, date)
    return t.astimezone(tzinfo)


def dusk(
    tzinfo: datetime.tzinfo,
    observer: Observer,
    date: Optional[datetime.date] = None,
    depression: float = 6.0,
) -> datetime.datetime:
    t = astral.utc.dusk(observer, date, depression)
    return t.astimezone(tzinfo)


def daylight(
    tzinfo: datetime.tzinfo, observer: Observer, date: Optional[datetime.date] = None
) -> Tuple[datetime.datetime, datetime.datetime]:
    t0, t1 = astral.utc.daylight(observer, date)
    return t0.astimezone(tzinfo), t1.astimezone(tzinfo)


def night(
    tzinfo: datetime.tzinfo, observer: Observer, date: Optional[datetime.date] = None
) -> Tuple[datetime.datetime, datetime.datetime]:
    t0, t1 = astral.utc.night(observer, date)
    return t0.astimezone(tzinfo), t1.astimezone(tzinfo)


def time_at_altitude(
    tzinfo: datetime.tzinfo,
    observer: Observer,
    altitude: float,
    date: datetime.date = None,
    direction: SunDirection = SunDirection.RISING,
) -> datetime.datetime:
    t = astral.utc.time_at_altitude(observer, altitude, date, direction)
    return t.astimezone(tzinfo)


def twilight(
    tzinfo: datetime.tzinfo,
    observer: Observer,
    date: Optional[datetime.date] = None,
    direction: SunDirection = SunDirection.RISING,
) -> Tuple[datetime.datetime, datetime.datetime]:
    t0, t1 = astral.utc.twilight(observer, date, direction)
    return t0.astimezone(tzinfo), t1.astimezone(tzinfo)


def golden_hour(
    tzinfo: datetime.tzinfo,
    observer: Observer,
    date: Optional[datetime.date] = None,
    direction: SunDirection = SunDirection.RISING,
) -> Tuple[datetime.datetime, datetime.datetime]:
    t0, t1 = astral.utc.golden_hour(observer, date, direction)
    return t0.astimezone(tzinfo), t1.astimezone(tzinfo)


def blue_hour(
    tzinfo: datetime.tzinfo,
    observer: Observer,
    date: Optional[datetime.date] = None,
    direction: SunDirection = SunDirection.RISING,
) -> Tuple[datetime.datetime, datetime.datetime]:
    t0, t1 = astral.utc.blue_hour(observer, date, direction)
    return t0.astimezone(tzinfo), t1.astimezone(tzinfo)


def rahukaalam(
    tzinfo: datetime.tzinfo,
    observer: Observer,
    date: Optional[datetime.date] = None,
    daytime: bool = True,
) -> Tuple[datetime.datetime, datetime.datetime]:
    t0, t1 = astral.utc.rahukaalam(observer, date, daytime)
    return t0.astimezone(tzinfo), t1.astimezone(tzinfo)


def sun(
    tzinfo: datetime.tzinfo,
    observer: Observer,
    date: Optional[datetime.date] = None,
    dawn_dusk_depression: float = 6.0,
) -> Dict:
    s = astral.utc.sun(observer, date, dawn_dusk_depression)
    return {key: s[key].astimezone(tzinfo) for key in s}
