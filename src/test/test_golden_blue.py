# -*- coding: utf-8 -*-
# Test data taken from http://www.timeanddate.com/sun/uk/london

import pytz
import datetime
from astral import sun
from astral.sun import SunDirection


def datetime_almost_equal(datetime1, datetime2, seconds=60):
    dd = datetime1 - datetime2
    sd = (dd.days * 24 * 60 * 60) + dd.seconds
    return abs(sd) <= seconds


def test_Location_GoldenHour_Morning(new_delhi):
    test_data = {
        datetime.date(2015, 12, 1): (
            datetime.datetime(2015, 12, 1, 1, 10, 10),
            datetime.datetime(2015, 12, 1, 2, 0, 43),
        ),
        datetime.date(2016, 1, 1): (
            datetime.datetime(2016, 1, 1, 1, 27, 46),
            datetime.datetime(2016, 1, 1, 2, 19, 1),
        ),
    }

    for day, golden_hour in test_data.items():
        start1 = pytz.utc.localize(golden_hour[0])
        end1 = pytz.utc.localize(golden_hour[1])

        start2, end2 = sun.golden_hour(new_delhi, day, SunDirection.RISING)
        assert datetime_almost_equal(end1, end2, seconds=90)
        assert datetime_almost_equal(start1, start2, seconds=90)


def test_Location_GoldenHour_Evening(london):
    test_data = {
        datetime.date(2016, 5, 18): (
            datetime.datetime(2016, 5, 18, 19, 1),
            datetime.datetime(2016, 5, 18, 20, 17),
        )
    }

    for day, golden_hour in test_data.items():
        start1 = pytz.utc.localize(golden_hour[0])
        end1 = pytz.utc.localize(golden_hour[1])

        start2, end2 = sun.golden_hour(london, day, SunDirection.SETTING)
        assert datetime_almost_equal(end1, end2, seconds=60)
        assert datetime_almost_equal(start1, start2, seconds=60)


def test_Location_BlueHour_Morning(london):
    test_data = {
        datetime.date(2016, 5, 19): (
            datetime.datetime(2016, 5, 19, 3, 19),
            datetime.datetime(2016, 5, 19, 3, 36),
        )
    }

    for day, blue_hour in test_data.items():
        start1 = pytz.utc.localize(blue_hour[0])
        end1 = pytz.utc.localize(blue_hour[1])

        start2, end2 = sun.blue_hour(london, day, SunDirection.RISING)
        assert datetime_almost_equal(end1, end2, seconds=90)
        assert datetime_almost_equal(start1, start2, seconds=90)


def test_Location_BlueHour_Evening(london):
    test_data = {
        datetime.date(2016, 5, 19): (
            datetime.datetime(2016, 5, 19, 20, 18),
            datetime.datetime(2016, 5, 19, 20, 35),
        )
    }

    for day, blue_hour in test_data.items():
        start1 = pytz.utc.localize(blue_hour[0])
        end1 = pytz.utc.localize(blue_hour[1])

        start2, end2 = sun.blue_hour(london, day, SunDirection.SETTING)
        assert datetime_almost_equal(end1, end2, seconds=90)
        assert datetime_almost_equal(start1, start2, seconds=90)
