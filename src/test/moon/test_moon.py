# -*- coding: utf-8 -*-
import datetime

import pytest

try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo

from almost_equal import datetime_almost_equal

from astral import moon
from astral.location import Location


@pytest.mark.parametrize(
    "date_,phase",
    [
        (datetime.date(2015, 12, 1), 19.477889),
        (datetime.date(2015, 12, 2), 20.333444),
        (datetime.date(2015, 12, 3), 21.189000),
        (datetime.date(2014, 12, 1), 9.0556666),
        (datetime.date(2014, 12, 2), 10.066777),
        (datetime.date(2014, 1, 1), 27.955666),
    ],
)
def test_moon_phase(date_: datetime.date, phase: float):
    """Test moon phase calculation"""
    assert moon.phase(date_) == pytest.approx(phase, abs=0.001)  # type: ignore


@pytest.mark.parametrize(
    "date_,risetime",
    [
        (datetime.date(2022, 11, 30), datetime.datetime(2022, 11, 30, 13, 17, 0)),
        (datetime.date(2022, 1, 1), datetime.datetime(2022, 1, 1, 6, 55, 0)),
        (datetime.date(2022, 2, 1), datetime.datetime(2022, 2, 1, 8, 24, 0)),
    ],
)
def test_moonrise_utc(
    date_: datetime.date, risetime: datetime.datetime, london: Location
):
    risetime = risetime.replace(tzinfo=london.tzinfo)
    calc_time = moon.moonrise(london.observer, date_)
    assert calc_time is not None
    assert datetime_almost_equal(calc_time, risetime, seconds=300)


@pytest.mark.parametrize(
    "date_,settime",
    [
        (datetime.date(2021, 10, 28), datetime.datetime(2021, 10, 28, 14, 11, 0)),
        (datetime.date(2021, 11, 6), datetime.datetime(2021, 11, 6, 17, 21, 0)),
        (datetime.date(2022, 2, 1), datetime.datetime(2022, 2, 1, 16, 57, 0)),
    ],
)
def test_moonset_utc(
    date_: datetime.date, settime: datetime.datetime, london: Location
):
    settime = settime.replace(tzinfo=datetime.timezone.utc)
    calc_time = moon.moonset(london.observer, date_)
    assert calc_time is not None
    assert datetime_almost_equal(calc_time, settime, seconds=180)


@pytest.mark.parametrize(
    "date_,risetime",
    [
        (datetime.date(2022, 5, 1), datetime.datetime(2022, 5, 1, 2, 34, 0)),
        (datetime.date(2022, 5, 24), datetime.datetime(2022, 5, 24, 22, 59, 0)),
    ],
)
def test_moonrise_riyadh_utc(
    date_: datetime.date, risetime: datetime.datetime, riyadh: Location
):
    risetime = risetime.replace(tzinfo=datetime.timezone.utc)
    calc_time = moon.moonrise(riyadh.observer, date_)
    assert calc_time is not None
    assert datetime_almost_equal(calc_time, risetime, seconds=180)


@pytest.mark.parametrize(
    "date_,settime",
    [
        (datetime.date(2021, 10, 28), datetime.datetime(2021, 10, 28, 9, 26, 0)),
        (datetime.date(2021, 11, 6), datetime.datetime(2021, 11, 6, 15, 33, 0)),
        (datetime.date(2022, 2, 1), datetime.datetime(2022, 2, 1, 14, 54, 0)),
    ],
)
def test_moonset_riyadh_utc(
    date_: datetime.date, settime: datetime.datetime, riyadh: Location
):
    settime = settime.replace(tzinfo=datetime.timezone.utc)
    calc_time = moon.moonset(riyadh.observer, date_)
    assert calc_time is not None
    assert datetime_almost_equal(calc_time, settime, seconds=180)


@pytest.mark.parametrize(
    "date_,risetime",
    [
        (datetime.date(2021, 10, 28), datetime.datetime(2021, 10, 28, 2, 6, 0)),
        (datetime.date(2021, 11, 6), datetime.datetime(2021, 11, 6, 6, 45, 0)),
    ],
)
def test_moonrise_wellington(
    date_: datetime.date, risetime: datetime.datetime, wellington: Location
):
    risetime = risetime.replace(tzinfo=wellington.tz)
    calc_time = moon.moonrise(wellington.observer, date_, tzinfo=wellington.tz)
    assert calc_time is not None
    calc_time = calc_time.astimezone(wellington.tzinfo)
    assert datetime_almost_equal(calc_time, risetime, seconds=120)


@pytest.mark.parametrize(
    "date_,settime",
    [
        (datetime.date(2021, 8, 18), datetime.datetime(2021, 8, 18, 3, 31, 0)),
        (datetime.date(2021, 7, 8), datetime.datetime(2021, 7, 8, 15, 16, 0)),
    ],
)
def test_moonset_wellington(
    date_: datetime.date, settime: datetime.datetime, wellington: Location
):
    settime = settime.replace(tzinfo=wellington.tzinfo)
    calc_time = moon.moonset(wellington.observer, date_, wellington.tzinfo)
    assert calc_time is not None
    calc_time = calc_time.astimezone(wellington.tzinfo)
    assert datetime_almost_equal(calc_time, settime, seconds=120)


# @pytest.mark.parametrize(
#     "longitude,jd",
#     [
#         (datetime.date(2021, 10, 28), datetime.datetime(2021, 10, 28, 13, 48, 0)),
#         (datetime.date(2021, 11, 6), datetime.datetime(2021, 11, 6, 7, 27, 0)),
#         # (datetime.date(2022, 2, 1), datetime.datetime(2022, 2, 1, 8, 24, 0)),
#     ],
# )
# def test_moon_local_sidereal_time(longitude: float, jd: float):
#     moon.local_sidereal_time(longitude, jd)
