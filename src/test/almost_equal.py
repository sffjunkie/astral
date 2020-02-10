from datetime import datetime

import pytz


def datetime_almost_equal(datetime1: datetime, datetime2: datetime, seconds: int = 60):
    if not (datetime1.tzinfo):
        datetime1 = pytz.utc.localize(datetime1)
    else:
        datetime1 = datetime1.astimezone(pytz.utc)

    if not (datetime2.tzinfo):
        datetime2 = pytz.utc.localize(datetime2)
    else:
        datetime2 = datetime2.astimezone(pytz.utc)

    dd = datetime1 - datetime2
    sd = (dd.days * 24 * 60 * 60) + dd.seconds
    return abs(sd) <= seconds
