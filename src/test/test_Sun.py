# -*- coding: utf-8 -*-
# Test data taken from http://www.timeanddate.com/sun/uk/london

import os
import sys
sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pytz
import datetime
from astral import Astral, AstralError, SUN_RISING, SUN_SETTING


def float_almost_equal(value1, value2, diff=0.5):
    return abs(value1 - value2) <= diff


def datetime_almost_equal(datetime1, datetime2, seconds=60):
    dd = datetime1 - datetime2
    sd = (dd.days * 24 * 60 * 60) + dd.seconds
    return abs(sd) <= seconds


def test_Astral_Dawn_Civil():
    a = Astral()
    l = a['London']

    test_data = {
        datetime.date(2015, 12, 1): datetime.datetime(2015, 12, 1, 7, 4),
        datetime.date(2015, 12, 2): datetime.datetime(2015, 12, 2, 7, 6),
        datetime.date(2015, 12, 3): datetime.datetime(2015, 12, 3, 7, 7),
        datetime.date(2015, 12, 12): datetime.datetime(2015, 12, 12, 7, 17),
        datetime.date(2015, 12, 25): datetime.datetime(2015, 12, 25, 7, 25),
    }

    for day, dawn in test_data.items():    
        dawn = pytz.UTC.localize(dawn)
        dawn_utc = a.dawn_utc(day, l.latitude, l.longitude)
        assert datetime_almost_equal(dawn, dawn_utc)


def test_Astral_Dawn_Nautical():
    a = Astral()
    a.solar_depression = 'nautical'
    l = a['London']

    test_data = {
        datetime.date(2015, 12, 1): datetime.datetime(2015, 12, 1, 6, 22),
        datetime.date(2015, 12, 2): datetime.datetime(2015, 12, 2, 6, 23),
        datetime.date(2015, 12, 3): datetime.datetime(2015, 12, 3, 6, 24),
        datetime.date(2015, 12, 12): datetime.datetime(2015, 12, 12, 6, 34),
        datetime.date(2015, 12, 25): datetime.datetime(2015, 12, 25, 6, 42),
    }

    for day, dawn in test_data.items():    
        dawn = pytz.UTC.localize(dawn)
        dawn_utc = a.dawn_utc(day, l.latitude, l.longitude)
        assert datetime_almost_equal(dawn, dawn_utc)


def test_Astral_Sunrise():
    a = Astral()
    l = a['London']

    test_data = {
        datetime.date(2015, 1, 1): datetime.datetime(2015, 1, 1, 8, 6),
        datetime.date(2015, 12, 1): datetime.datetime(2015, 12, 1, 7, 43),
        datetime.date(2015, 12, 2): datetime.datetime(2015, 12, 2, 7, 45),
        datetime.date(2015, 12, 3): datetime.datetime(2015, 12, 3, 7, 46),
        datetime.date(2015, 12, 12): datetime.datetime(2015, 12, 12, 7, 57),
        datetime.date(2015, 12, 25): datetime.datetime(2015, 12, 25, 8, 5),
    }

    for day, sunrise in test_data.items():    
        sunrise = pytz.UTC.localize(sunrise)
        sunrise_utc = a.sunrise_utc(day, l.latitude, l.longitude)
        assert datetime_almost_equal(sunrise, sunrise_utc)


def test_Astral_Sunset():
    a = Astral()
    l = a['London']

    test_data = {
        datetime.date(2015, 1, 1): datetime.datetime(2015, 1, 1, 16, 2),
        datetime.date(2015, 12, 1): datetime.datetime(2015, 12, 1, 15, 55),
        datetime.date(2015, 12, 2): datetime.datetime(2015, 12, 2, 15, 55),
        datetime.date(2015, 12, 3): datetime.datetime(2015, 12, 3, 15, 54),
        datetime.date(2015, 12, 12): datetime.datetime(2015, 12, 12, 15, 51),
        datetime.date(2015, 12, 25): datetime.datetime(2015, 12, 25, 15, 56),
    }

    for day, sunset in test_data.items():    
        sunset = pytz.UTC.localize(sunset)
        sunset_utc = a.sunset_utc(day, l.latitude, l.longitude)
        assert datetime_almost_equal(sunset, sunset_utc)


def test_Astral_Dusk_Civil():
    a = Astral()
    l = a['London']

    test_data = {
        datetime.date(2015, 12, 1): datetime.datetime(2015, 12, 1, 16, 34),
        datetime.date(2015, 12, 2): datetime.datetime(2015, 12, 2, 16, 34),
        datetime.date(2015, 12, 3): datetime.datetime(2015, 12, 3, 16, 33),
        datetime.date(2015, 12, 12): datetime.datetime(2015, 12, 12, 16, 31),
        datetime.date(2015, 12, 25): datetime.datetime(2015, 12, 25, 16, 36),
    }

    for day, dusk in test_data.items():    
        dusk = pytz.UTC.localize(dusk)
        dusk_utc = a.dusk_utc(day, l.latitude, l.longitude)
        assert datetime_almost_equal(dusk, dusk_utc)


def test_Astral_Dusk_Nautical():
    a = Astral()
    a.solar_depression = 'nautical'
    l = a['London']

    test_data = {
        datetime.date(2015, 12, 1): datetime.datetime(2015, 12, 1, 17, 16),
        datetime.date(2015, 12, 2): datetime.datetime(2015, 12, 2, 17, 16),
        datetime.date(2015, 12, 3): datetime.datetime(2015, 12, 3, 17, 16),
        datetime.date(2015, 12, 12): datetime.datetime(2015, 12, 12, 17, 14),
        datetime.date(2015, 12, 25): datetime.datetime(2015, 12, 25, 17, 19),
    }

    for day, dusk in test_data.items():    
        dusk = pytz.UTC.localize(dusk)
        dusk_utc = a.dusk_utc(day, l.latitude, l.longitude)
        assert datetime_almost_equal(dusk, dusk_utc)


def test_Astral_SolarNoon():
    a = Astral()
    l = a['London']

    test_data = {
        datetime.date(2015, 12, 1): datetime.datetime(2015, 12, 1, 11, 49),
        datetime.date(2015, 12, 2): datetime.datetime(2015, 12, 2, 11, 50),
        datetime.date(2015, 12, 3): datetime.datetime(2015, 12, 3, 11, 50),
        datetime.date(2015, 12, 12): datetime.datetime(2015, 12, 12, 11, 54),
        datetime.date(2015, 12, 25): datetime.datetime(2015, 12, 25, 12, 00),
    }

    for day, solar_noon in test_data.items():    
        solar_noon = pytz.UTC.localize(solar_noon)
        solar_noon_utc = a.solar_noon_utc(day, l.longitude)
        assert datetime_almost_equal(solar_noon, solar_noon_utc)


# Test data from http://www.astroloka.com/rahukaal.aspx?City=Delhi
def test_Astral_Rahukaalam():
    a = Astral()
    l = a['New Delhi']
    
    test_data = {
        datetime.date(2015, 12, 1): (datetime.datetime(2015, 12, 1, 9, 17), datetime.datetime(2015, 12, 1, 10, 35)),
        datetime.date(2015, 12, 2): (datetime.datetime(2015, 12, 2, 6, 40), datetime.datetime(2015, 12, 2, 7, 58)),
    }
    
    for day, (start, end) in test_data.items():
        start = pytz.UTC.localize(start)
        end = pytz.UTC.localize(end)
        
        info = a.rahukaalam_utc(day, l.latitude, l.longitude)
        start_utc = info[0]
        end_utc = info[1]
        assert datetime_almost_equal(start, start_utc)
        assert datetime_almost_equal(end, end_utc)


def test_Astral_SolarElevation():
    a = Astral()
    l = a['London']

    test_data = {
        datetime.datetime(2015, 12, 14, 11, 0, 0): 14,
        datetime.datetime(2015, 12, 14, 20, 1, 0): -37,
    }
    
    for dt, angle1 in test_data.items():
        angle2 = a.solar_elevation(dt, l.latitude, l.longitude)
        assert float_almost_equal(angle1, angle2)


def test_Astral_SolarAzimuth():
    a = Astral()
    l = a['London']

    test_data = {
        datetime.datetime(2015, 12, 14, 11, 0, 0, tzinfo=pytz.UTC): 167,
        datetime.datetime(2015, 12, 14, 20, 1, 0): 279,
    }
    
    for dt, angle1 in test_data.items():
        angle2 = a.solar_azimuth(dt, l.latitude, l.longitude)
        assert float_almost_equal(angle1, angle2)


def test_Astral_TimeAtElevation_SunRising():
    a = Astral()
    l = a['London']

    d = datetime.date(2016, 1, 4)
    dt = a.time_at_elevation_utc(6, SUN_RISING, d, l.latitude, l.longitude)
    cdt = datetime.datetime(2016, 1, 4, 9, 5, 0, tzinfo=pytz.UTC)
    # Use error of 5 minutes as website has a rather coarse accuracy
    assert datetime_almost_equal(dt, cdt, 300)


def test_Astral_TimeAtElevation_SunSetting():
    a = Astral()
    l = a['London']

    d = datetime.date(2016, 1, 4)
    dt = a.time_at_elevation_utc(14, SUN_SETTING, d, l.latitude, l.longitude)
    cdt = datetime.datetime(2016, 1, 4, 13, 20, 0, tzinfo=pytz.UTC)
    assert datetime_almost_equal(dt, cdt, 300)


def test_Astral_TimeAtElevation_GreaterThan90():
    a = Astral()
    l = a['London']

    d = datetime.date(2016, 1, 4)
    dt = a.time_at_elevation_utc(166, SUN_RISING, d, l.latitude, l.longitude)
    cdt = datetime.datetime(2016, 1, 4, 13, 20, 0, tzinfo=pytz.UTC)
    assert datetime_almost_equal(dt, cdt, 300)


def test_Astral_TimeAtElevation_GreaterThan180():
    a = Astral()
    l = a['London']

    d = datetime.date(2015, 12, 1)
    dt = a.time_at_elevation_utc(186, SUN_RISING, d, l.latitude, l.longitude)
    cdt = datetime.datetime(2015, 12, 1, 16, 34, tzinfo=pytz.UTC)
    assert datetime_almost_equal(dt, cdt, 300)


def test_Astral_TimeAtElevation_SunRisingBelowHorizon():
    a = Astral()
    l = a['London']

    d = datetime.date(2016, 1, 4)
    dt = a.time_at_elevation_utc(-18, SUN_RISING, d, l.latitude, l.longitude)
    cdt = datetime.datetime(2016, 1, 4, 6, 0, 0, tzinfo=pytz.UTC)
    assert datetime_almost_equal(dt, cdt, 300)


def test_Astral_TimeAtElevation_BadElevation():
    a = Astral()
    l = a['London']

    d = datetime.date(2016, 1, 4)
    with pytest.raises(AstralError):
        a.time_at_elevation_utc(20, SUN_RISING, d, l.latitude, l.longitude)


def test_Astral_Daylight():
    a = Astral()
    l = a['London']

    d = datetime.date(2016, 1, 6)
    start, end = a.daylight_utc(d, l.latitude, l.longitude)
    cstart = datetime.datetime(2016, 1, 6, 8, 5, 0, tzinfo=pytz.UTC)
    cend = datetime.datetime(2016, 1, 6, 16, 7, 0, tzinfo=pytz.UTC)
    assert datetime_almost_equal(start, cstart, 300)
    assert datetime_almost_equal(end, cend, 300)


def test_Astral_Nighttime():
    a = Astral()
    l = a['London']

    d = datetime.date(2016, 1, 6)
    start, end = a.night_utc(d, l.latitude, l.longitude)
    cstart = datetime.datetime(2016, 1, 6, 18, 10, 0, tzinfo=pytz.UTC)
    cend = datetime.datetime(2016, 1, 7, 6, 2, 0, tzinfo=pytz.UTC)
    assert datetime_almost_equal(start, cstart, 300)
    assert datetime_almost_equal(end, cend, 300)
