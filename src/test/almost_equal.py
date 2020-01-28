from datetime import datetime

import pytz

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
