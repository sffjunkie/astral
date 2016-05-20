# -*- coding: utf-8 -*-
# Test data taken from http://www.timeanddate.com/sun/uk/london

import os
import sys
sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytz
import datetime
from astral import Astral, SUN_RISING, SUN_SETTING


def datetime_almost_equal(datetime1, datetime2, seconds=60):
    dd = datetime1 - datetime2
    sd = (dd.days * 24 * 60 * 60) + dd.seconds
    return abs(sd) <= seconds


def test_Location_GoldenHour_Morning():
    a = Astral()
    l = a['London']

    test_data = {
        datetime.date(2016, 5, 18): (datetime.datetime(2016, 5, 18, 3, 37),
                                     datetime.datetime(2016, 5, 18, 4, 53)),
        datetime.date(2016, 1, 1): (datetime.datetime(2016, 1, 1, 7, 41),
                                    datetime.datetime(2016, 1, 1, 9, 7)),
    }

    for day, golden_hour in test_data.items():
        start1 = pytz.UTC.localize(golden_hour[0])
        end1 = pytz.UTC.localize(golden_hour[1])
        
        start2, end2 = l.golden_hour(SUN_RISING, day)
        assert datetime_almost_equal(end1, end2, seconds=90)
        assert datetime_almost_equal(start1, start2, seconds=90)


def test_Location_GoldenHour_Evening():
    a = Astral()
    l = a['London']

    test_data = {
        datetime.date(2016, 5, 18): (datetime.datetime(2016, 5, 18, 19, 0),
                                     datetime.datetime(2016, 5, 18, 20, 16)),
    }

    for day, golden_hour in test_data.items():
        start1 = pytz.UTC.localize(golden_hour[0])
        end1 = pytz.UTC.localize(golden_hour[1])
        
        start2, end2 = l.golden_hour(SUN_SETTING, day)
        assert datetime_almost_equal(end1, end2, seconds=90)
        assert datetime_almost_equal(start1, start2, seconds=90)


def test_Location_BlueHour_Morning():
    a = Astral()
    l = a['London']

    test_data = {
        datetime.date(2016, 5, 19): (datetime.datetime(2016, 5, 19, 3, 19),
                                     datetime.datetime(2016, 5, 19, 3, 36)),
    }

    for day, blue_hour in test_data.items():
        start1 = pytz.UTC.localize(blue_hour[0])
        end1 = pytz.UTC.localize(blue_hour[1])
        
        start2, end2 = l.blue_hour(SUN_RISING, day)
        assert datetime_almost_equal(end1, end2, seconds=90)
        assert datetime_almost_equal(start1, start2, seconds=90)


def test_Location_BlueHour_Evening():
    a = Astral()
    l = a['London']

    test_data = {
        datetime.date(2016, 5, 19): (datetime.datetime(2016, 5, 19, 20, 17),
                                     datetime.datetime(2016, 5, 19, 20, 34)),
    }

    for day, blue_hour in test_data.items():
        start1 = pytz.UTC.localize(blue_hour[0])
        end1 = pytz.UTC.localize(blue_hour[1])
        
        start2, end2 = l.blue_hour(SUN_SETTING, day)
        assert datetime_almost_equal(end1, end2, seconds=90)
        assert datetime_almost_equal(start1, start2, seconds=90)
