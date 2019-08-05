"""UTC date/time functions"""

import datetime

import pytz


__all__ = ["now", "today"]


def now() -> datetime.datetime:
    """Returns the current time in the UTC time zone"""
    return pytz.utc.localize(datetime.datetime.utcnow())


def today() -> datetime.date:
    """Returns the current date in the UTC time zone"""
    return now().date()
