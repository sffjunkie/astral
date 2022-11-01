import datetime
from pprint import pprint

from almost_equal import datetime_almost_equal

from astral.location import Location
from astral.sun import sun


def test_Wellington(wellington: Location):
    dt = datetime.date(2020, 2, 11)
    s = sun(wellington.observer, dt, tzinfo=wellington.tzinfo)
    assert datetime_almost_equal(
        s["sunrise"],
        datetime.datetime(2020, 2, 11, 6, 38, 42, tzinfo=wellington.tzinfo),
    )
    assert datetime_almost_equal(
        s["sunset"],
        datetime.datetime(2020, 2, 11, 20, 31, 00, tzinfo=wellington.tzinfo),
    )
