# -*- coding: utf-8 -*-
from nose.tools import raises

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

@raises(AttributeError)
def test_TzError():
    c = Location()
    c.tz = 1

if __name__ == "__main__":
    test_Name()
    test_Country()
    test_TimezoneName()
    test_Timezone()
    test_Dawn()
    test_Sunrise()
    test_SolarNoon()
    test_Dusk()
    test_Sunset()
    test_SolarElevation()
    test_SolarAzimuth()
    test_SolarDepression()
    test_Moon()
    