import datetime

from astral.location import Location
from astral.sun import sun

from almost_equal import datetime_almost_equal


def test_Wellington(wellington: Location):
    dt = datetime.date(2020, 2, 11)
    s = sun(wellington.observer, dt, tzinfo=wellington.tzinfo)
    assert datetime_almost_equal(
        s["sunrise"],
        datetime.datetime(2020, 2, 11, 6, 38, 42, tzinfo=wellington.tzinfo),
    )
