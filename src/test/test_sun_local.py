import datetime

import pytest
from almost_equal import datetime_almost_equal

from astral import sun
from astral.location import Location


@pytest.mark.parametrize(
    "day,dawn",
    [
        (datetime.date(2015, 12, 1), datetime.datetime(2015, 12, 1, 6, 30)),
        (datetime.date(2015, 12, 2), datetime.datetime(2015, 12, 2, 6, 31)),
        (datetime.date(2015, 12, 3), datetime.datetime(2015, 12, 3, 6, 31)),
        (datetime.date(2015, 12, 12), datetime.datetime(2015, 12, 12, 6, 38)),
        (datetime.date(2015, 12, 25), datetime.datetime(2015, 12, 25, 6, 45)),
    ],
)
def test_Sun_Local_tzinfo(
    day: datetime.date, dawn: datetime.datetime, new_delhi: Location
):
    dawn = dawn.replace(tzinfo=new_delhi.tzinfo)
    dawn_calc = sun.sun(new_delhi.observer, day, 6.0, new_delhi.tzinfo)["dawn"]
    assert datetime_almost_equal(dawn, dawn_calc)


@pytest.mark.parametrize(
    "day,dawn",
    [
        (datetime.date(2015, 12, 1), datetime.datetime(2015, 12, 1, 6, 30)),
        (datetime.date(2015, 12, 2), datetime.datetime(2015, 12, 2, 6, 31)),
        (datetime.date(2015, 12, 3), datetime.datetime(2015, 12, 3, 6, 31)),
        (datetime.date(2015, 12, 12), datetime.datetime(2015, 12, 12, 6, 38)),
        (datetime.date(2015, 12, 25), datetime.datetime(2015, 12, 25, 6, 45)),
    ],
)
def test_Sun_Local_str(
    day: datetime.date, dawn: datetime.datetime, new_delhi: Location
):
    dawn = dawn.replace(tzinfo=new_delhi.tzinfo)
    dawn_calc = sun.sun(new_delhi.observer, day, 6.0, "Asia/Kolkata")["dawn"]
    assert datetime_almost_equal(dawn, dawn_calc)
