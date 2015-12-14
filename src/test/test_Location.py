# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pytest import raises

from astral import Astral, Location
import datetime
import pytz

def test_Location_Name():
    c = Location()
    assert c.name == 'Greenwich'
    c.name = 'London'
    assert c.name == 'London'
    c.name = 'Köln'
    assert c.name == 'Köln'


def test_Location_Country():
    c = Location()
    assert c.region == 'England'
    c.region = 'Australia'
    assert c.region == 'Australia'


def test_Location_TimezoneName():
    c = Location()
    assert c.timezone == 'Europe/London'
    c.name = 'Asia/Riyadh'
    assert c.name == 'Asia/Riyadh'


def test_Location_Timezone():
    c = Location()
    assert c.tz == pytz.timezone('Europe/London')
    c.timezone='Europe/Stockholm'
    assert c.tz == pytz.timezone('Europe/Stockholm')


def test_Location_Dawn():
    c = Location()
    c.dawn()


def test_Location_Sunrise():
    c = Location()
    c.sunrise()


def test_Location_SolarNoon():
    c = Location()
    c.solar_noon()


def test_Location_Dusk():
    c = Location()
    c.dusk()


def test_Location_Sunset():
    c = Location()
    c.sunset()


def test_Location_SolarElevation():
    dd = Astral()
    location = dd['Riyadh']
    dt = datetime.datetime(2015, 12, 14, 8, 0, 0)
    dt = location.tz.localize(dt)
    elevation = location.solar_elevation(dt)
    assert abs(elevation - 17) < 0.5


def test_Location_SolarAzimuth():
    dd = Astral()
    location = dd['Riyadh']
    dt = datetime.datetime(2015, 12, 14, 8, 0, 0)
    dt = location.tz.localize(dt)
    azimuth = location.solar_azimuth(dt)
    assert abs(azimuth - 126) < 0.5

    
def test_Location_SolarDepression():
    c = Location(("Heidelberg", "Germany", 49.412, -8.71, "Europe/Berlin"))
    c.solar_depression = 'nautical'
    assert c.solar_depression == 12
    
    c.solar_depression = 18
    assert c.solar_depression == 18

    
def test_Location_Moon():
    c=Location()
    c.moon_phase()


def test_Location_TzError():
    with raises(AttributeError):
        c = Location()
        c.tz = 1
