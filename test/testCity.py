from nose.tools import raises

import datetime
import pytz
from astral import City

def testName():
    c = City()
    assert c.name == 'Greenwich'
    c.name = 'London'
    assert c.name == 'London'

def testCountry():
    c = City()
    assert c.country == 'England'
    c.country = 'Australia'
    assert c.country == 'Australia'

def testTimezoneName():
    c = City()
    assert c.timezone == 'Europe/London'
    c.name = 'Asia/Riyadh'
    assert c.name == 'Asia/Riyadh'

def testTimezone():
    c = City()
    assert c.tz == pytz.timezone('Europe/London')
    c.timezone='Europe/Stockholm'
    assert c.tz == pytz.timezone('Europe/Stockholm')

def testDawn():
    c = City()
    c.dawn()

def testSunrise():
    c = City()
    c.sunrise()

def testSolarNoon():
    c = City()
    c.solar_noon()

def testDusk():
    c = City()
    c.dusk()

def testSunset():
    c = City()
    c.sunset()
    
def testElevation():
    c = City()
    c.solar_elevation()
    
def testAzimuth():
    c = City()
    c.solar_azimuth()

@raises(AttributeError)
def testTzError():
    c = City()
    c.tz = 1

