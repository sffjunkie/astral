import datetime

import pytz
from astral.geocoder import database, lookup
from astral.sun import sun

from almost_equal import datetime_almost_equal


def test_Wellington():
    wellington = lookup("Wellington", database())
    dt = datetime.date(2020, 2, 11)
    tz = pytz.timezone(wellington.timezone)
    s = sun(wellington.observer, dt, tzinfo=tz)
    assert datetime_almost_equal(
        s["sunrise"], tz.localize(datetime.datetime(2020, 2, 11, 6, 38, 42))
    )
