"""Local date/time functions"""

import datetime

import pytz

__all__ = ["now", "today"]


def now(tzinfo: datetime.tzinfo) -> datetime.datetime:
    """Returns the current local time in a time zone"""
    return pytz.utc.localize(datetime.datetime.utcnow()).astimezone(tzinfo)


def today(tzinfo: datetime.tzinfo) -> datetime.date:
    """Returns the current local date in a time zone"""
    return now(tzinfo).date()
