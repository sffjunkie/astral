# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pytest import raises

import datetime
from astral import Astral


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


def test_AstralSolarElevation():
    dd = Astral()
    dt = datetime.datetime(2015, 2, 3, 9, 0, 0)

    elevation = dd.solar_elevation(dt, 51.5, -0.12)
    assert abs(elevation - 9.97) < 0.1


def test_AstralSolarAzimuth():
    dd = Astral()
    dt = datetime.datetime(2015, 2, 3, 9, 0, 0)

    azimuth = dd.solar_azimuth(dt, 51.5, -0.12)
    assert abs(azimuth - 133.162) < 0.1


def test_AstralSolarElevationWithTimezone():
    dd = Astral()
    location = dd['Jubail']

    dt = datetime.datetime(2015, 2, 4, 9, 0, 0, tzinfo=location.tz)
    elevation = dd.solar_elevation(dt, location.latitude, location.longitude)
    assert abs(elevation - 28.118) < 0.1


def test_AstralSolarAzimuthWithTimezone():
    dd = Astral()
    location = dd['Jubail']

    dt = datetime.datetime(2015, 2, 4, 9, 0, 0, tzinfo=location.tz)
    azimuth = dd.solar_azimuth(dt, location.latitude, location.longitude)
    assert abs(azimuth - 129.02) < 0.1


def test_LocationSolarElevation():
    dd = Astral()
    location = dd['Jubail']
    dt = datetime.datetime(2015, 2, 4, 9, 0, 0)
    elevation = location.solar_elevation(dt)
    assert abs(elevation - 28.118) < 0.1


def test_LocationSolarAzimuth():
    dd = Astral()
    location = dd['Jubail']
    dt = datetime.datetime(2015, 2, 4, 9, 0, 0)
    azimuth = location.solar_azimuth(dt)
    assert abs(azimuth - 129.02) < 0.1


def test_Moon():
    dd = Astral()
    phase = dd.moon_phase(datetime.date(2011, 2, 25))
    assert phase == 21


def test_Elevation():
    dd = Astral()
    c = dd['London']

    assert c.elevation == 24
