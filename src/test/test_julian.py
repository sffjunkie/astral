import datetime
from typing import Union

import pytest
from almost_equal import datetime_almost_equal

from astral.julian import (
    Calendar,
    juliancentury_to_julianday,
    julianday,
    julianday_to_datetime,
    julianday_to_juliancentury,
)


@pytest.mark.parametrize(
    "day,jd",
    [
        (datetime.datetime(1957, 10, 4, 19, 26, 24), 2436116.31),
        (datetime.date(2000, 1, 1), 2451544.5),
        (datetime.date(2012, 1, 1), 2455927.5),
        (datetime.date(2013, 1, 1), 2456293.5),
        (datetime.date(2013, 6, 1), 2456444.5),
        (datetime.date(1867, 2, 1), 2402998.5),
        (datetime.date(3200, 11, 14), 2890153.5),
        (datetime.datetime(2000, 1, 1, 12, 0, 0), 2451545.0),
        (datetime.datetime(1999, 1, 1, 0, 0, 0), 2451179.5),
        (datetime.datetime(1987, 1, 27, 0, 0, 0), 2446_822.5),
        (datetime.date(1987, 6, 19), 2446_965.5),
        (datetime.datetime(1987, 6, 19, 12, 0, 0), 2446_966.0),
        (datetime.datetime(1988, 1, 27, 0, 0, 0), 2447_187.5),
        (datetime.date(1988, 6, 19), 2447_331.5),
        (datetime.datetime(1988, 6, 19, 12, 0, 0), 2447_332.0),
        (datetime.datetime(1900, 1, 1, 0, 0, 0), 2415_020.5),
        (datetime.datetime(1600, 1, 1, 0, 0, 0), 2305_447.5),
        (datetime.datetime(1600, 12, 31, 0, 0, 0), 2305_812.5),
        (datetime.datetime(2012, 1, 1, 12), 2455928.0),
        (datetime.date(2013, 1, 1), 2456293.5),
        (datetime.date(2013, 6, 1), 2456444.5),
        (datetime.date(1867, 2, 1), 2402998.5),
        (datetime.date(3200, 11, 14), 2890153.5),
    ],
)
def test_JulianDay(day: Union[datetime.date, datetime.datetime], jd: float):
    assert julianday(day) == jd


@pytest.mark.parametrize(
    "day,jd",
    [
        (datetime.datetime(837, 4, 10, 7, 12, 0), 2026_871.8),
        (datetime.datetime(333, 1, 27, 12, 0, 0), 1842_713.0),
    ],
)
def test_JulianDay_JulianCalendar(
    day: Union[datetime.date, datetime.datetime], jd: float
):
    assert julianday(day, Calendar.JULIAN) == jd


@pytest.mark.parametrize(
    "jd,dt",
    [
        (2026_871.8, datetime.datetime(837, 4, 10, 7, 12, 0)),
        (1842_713.0, datetime.datetime(333, 1, 27, 12, 0, 0)),
    ],
)
def test_JulianDay_ToDateTime(jd: float, dt: datetime.datetime):
    assert datetime_almost_equal(julianday_to_datetime(jd), dt)


@pytest.mark.parametrize(
    "jd,jc",
    [
        (2455927.5, 0.119986311),
        (2456293.5, 0.130006845),
        (2456444.5, 0.134140999),
        (2402998.5, -1.329130732),
        (2890153.5, 12.00844627),
    ],
)
def test_JulianCentury(jd: float, jc: float):
    assert julianday_to_juliancentury(jd) == pytest.approx(jc)


@pytest.mark.parametrize(
    "jc,jd",
    [
        (0.119986311, 2455927.5),
        (0.130006845, 2456293.5),
        (0.134140999, 2456444.5),
        (-1.329130732, 2402998.5),
        (12.00844627, 2890153.5),
    ],
)
def test_JulianCenturyToJulianDay(jc: float, jd: float):
    assert juliancentury_to_julianday(jc) == pytest.approx(jd)
