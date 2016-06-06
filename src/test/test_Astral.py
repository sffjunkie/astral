# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pytest import raises

import pytz
import datetime
from astral import Astral


def float_almost_equal(value1, value2, diff=0.5):
    return abs(value1 - value2) <= diff


def test_AstralBadLocationName():
    with raises(KeyError):
        dd = Astral()
        _c = dd['wally']


def test_AstralLocationName():
    dd = Astral()
    c = dd['London']
    assert c.name == 'London'


def test_AstralAssign():
    with raises(TypeError):
        dd = Astral()
        dd['London'] = 'wally'


def test_Astral():
    location_name = 'Jubail'

    dd = Astral()
    dd.solar_depression = 'civil'

    location = dd[location_name]
    assert location.timezone == 'Asia/Riyadh'

    sun = location.sun()
    sunrise = location.sunrise(local=True)
    assert sunrise == sun['sunrise']


def test_Astral_SolarElevation():
    dd = Astral()
    dt = datetime.datetime(2015, 2, 3, 9, 0, 0, tzinfo=pytz.UTC)

    elevation = dd.solar_elevation(dt, 51.5, -0.12)
    assert float_almost_equal(elevation, 9.97, 0.1)


def test_Astral_SolarAzimuth():
    dd = Astral()
    dt = datetime.datetime(2015, 2, 3, 9, 0, 0, tzinfo=pytz.UTC)

    azimuth = dd.solar_azimuth(dt, 51.5, -0.12)
    assert float_almost_equal(azimuth, 133.162, 0.1)


def test_Astral_SolarElevationWithTimezone():
    dd = Astral()
    location = dd['Jubail']

    dt = datetime.datetime(2015, 2, 4, 9, 0, 0, tzinfo=location.tz)
    elevation = dd.solar_elevation(dt, location.latitude, location.longitude)
    assert float_almost_equal(elevation, 28.118, 0.1)


def test_Astral_SolarAzimuthWithTimezone():
    dd = Astral()
    location = dd['Jubail']

    dt = datetime.datetime(2015, 2, 4, 9, 0, 0, tzinfo=location.tz)
    azimuth = dd.solar_azimuth(dt, location.latitude, location.longitude)
    assert float_almost_equal(azimuth, 129.02, 0.1)


def test_Astral_JulianDay():
    a = Astral()
    
    dt = datetime.date(2015, 1, 1)
    jd = a._julianday(dt)
    assert float_almost_equal(jd, 2457023.5, 0.1)
    
    dt = datetime.date(2015, 2, 9)
    jd = a._julianday(dt)
    assert float_almost_equal(jd, 2457062.5, 0.1)
    
    dt = datetime.date(2000, 8, 12)
    jd = a._julianday(dt)
    assert float_almost_equal(jd, 2451768.5, 0.1)
    
    dt = datetime.date(1632, 8, 12)
    jd = a._julianday(dt)
    assert float_almost_equal(jd, 2317359.5, 0.1)
    