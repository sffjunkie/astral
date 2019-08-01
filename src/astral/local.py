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
    observer: Observer,
    date: Optional[datetime.date] = None,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> datetime.datetime:
    t = astral.utc.solar_noon(observer, date)
    return t.astimezone(tzinfo)


def solar_midnight(
    observer: Observer,
    date: Optional[datetime.date] = None,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> datetime.datetime:
    t = astral.utc.solar_midnight(observer, date)
    return t.astimezone(tzinfo)


def dawn(
    observer: Observer,
    date: Optional[datetime.date] = None,
    depression: float = 6.0,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> datetime.datetime:
    return astral.utc.dawn(observer, date, depression).astimezone(tzinfo)


def sunrise(
    observer: Observer,
    date: Optional[datetime.date] = None,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> datetime.datetime:
    t = astral.utc.sunrise(observer, date)
    return t.astimezone(tzinfo)


def sunset(
    observer: Observer, date: Optional[datetime.date] = None,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> datetime.datetime:
    t = astral.utc.sunset(observer, date)
    return t.astimezone(tzinfo)


def dusk(
    observer: Observer,
    date: Optional[datetime.date] = None,
    depression: float = 6.0,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> datetime.datetime:
    t = astral.utc.dusk(observer, date, depression)
    return t.astimezone(tzinfo)


def daylight(
    observer: Observer, date: Optional[datetime.date] = None,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> Tuple[datetime.datetime, datetime.datetime]:
    t0, t1 = astral.utc.daylight(observer, date)
    return t0.astimezone(tzinfo), t1.astimezone(tzinfo)


def night(
    observer: Observer, date: Optional[datetime.date] = None,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> Tuple[datetime.datetime, datetime.datetime]:
    t0, t1 = astral.utc.night(observer, date)
    return t0.astimezone(tzinfo), t1.astimezone(tzinfo)


def time_at_altitude(
    observer: Observer,
    altitude: float,
    date: datetime.date = None,
    direction: SunDirection = SunDirection.RISING,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> datetime.datetime:
    t = astral.utc.time_at_altitude(observer, altitude, date, direction)
    return t.astimezone(tzinfo)


def twilight(
    observer: Observer,
    date: Optional[datetime.date] = None,
    direction: SunDirection = SunDirection.RISING,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> Tuple[datetime.datetime, datetime.datetime]:
    t0, t1 = astral.utc.twilight(observer, date, direction)
    return t0.astimezone(tzinfo), t1.astimezone(tzinfo)


def golden_hour(
    observer: Observer,
    date: Optional[datetime.date] = None,
    direction: SunDirection = SunDirection.RISING,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> Tuple[datetime.datetime, datetime.datetime]:
    t0, t1 = astral.utc.golden_hour(observer, date, direction)
    return t0.astimezone(tzinfo), t1.astimezone(tzinfo)


def blue_hour(
    observer: Observer,
    date: Optional[datetime.date] = None,
    direction: SunDirection = SunDirection.RISING,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> Tuple[datetime.datetime, datetime.datetime]:
    t0, t1 = astral.utc.blue_hour(observer, date, direction)
    return t0.astimezone(tzinfo), t1.astimezone(tzinfo)


def rahukaalam(
    observer: Observer,
    date: Optional[datetime.date] = None,
    daytime: bool = True,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> Tuple[datetime.datetime, datetime.datetime]:
    t0, t1 = astral.utc.rahukaalam(observer, date, daytime)
    return t0.astimezone(tzinfo), t1.astimezone(tzinfo)


def sun(
    observer: Observer,
    date: Optional[datetime.date] = None,
    dawn_dusk_depression: float = 6.0,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> Dict:
    s = astral.utc.sun(observer, date, dawn_dusk_depression)
    return {key: s[key].astimezone(tzinfo) for key in s}
