# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pytest import raises

import pytz
from astral import Location

def test_Name():
    c = Location()
    assert c.name == 'Greenwich'
    c.name = 'London'
    assert c.name == 'London'
    c.name = 'Köln'
    assert c.name == 'Köln'

def test_Country():
    c = Location()
    assert c.region == 'England'
    c.region = 'Australia'
    assert c.region == 'Australia'

def test_TimezoneName():
    c = Location()
    assert c.timezone == 'Europe/London'
    c.name = 'Asia/Riyadh'
    assert c.name == 'Asia/Riyadh'

def test_Timezone():
    c = Location()
    assert c.tz == pytz.timezone('Europe/London')
    c.timezone='Europe/Stockholm'
    assert c.tz == pytz.timezone('Europe/Stockholm')

def test_Dawn():
    c = Location()
    c.dawn()

def test_Sunrise():
    c = Location()
    c.sunrise()

def test_SolarNoon():
    c = Location()
    c.solar_noon()

def test_Dusk():
    c = Location()
    c.dusk()

def test_Sunset():
    c = Location()
    c.sunset()
    
def test_SolarElevation():
    c = Location()
    c.solar_elevation()
    
def test_SolarAzimuth():
    c = Location()
    c.solar_azimuth()
    
def test_SolarDepression():
    c = Location(("Heidelberg", "Germany", 49.412, -8.71, "Europe/Berlin"))
    c.solar_depression = 'nautical'
    assert c.solar_depression == 12
    
    c.solar_depression = 18
    assert c.solar_depression == 18
    
def test_Moon():
    c=Location()
    c.moon_phase()

def test_TzError():
    with raises(AttributeError):
        c = Location()
        c.tz = 1
