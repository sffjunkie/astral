# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pytest import raises

import datetime
import pytz
from astral import Astral, Location
    
def test_AstralBadLocationName():
    with raises(KeyError):
        dd = Astral()
        c = dd['wally']    

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
    
    print('Information for %s/%s\n' % (location_name, location.region))
    
    timezone = location.timezone
    print('Timezone: %s' % timezone)
    
    loc_tz = pytz.timezone(timezone)
    print('Latitude: %.02f; Longitude: %.02f\n' % (location.latitude, location.longitude))
    
    sun = location.sun()
    sunrise = location.sunrise(local=True)
    assert sunrise == sun['sunrise']

    rahukaalam = location.rahukaalam()

def test_SolarElevation():
    location_name = 'Jubail'
    
    dd = Astral()
    location=dd[location_name]

    dt = datetime.datetime.now(tz=location.tz)
    print('Date & time: %s' % dt)
    print('Date & time (UTC): %s' % dt.astimezone(pytz.utc))
    print('Elevation: %.02f' % dd.solar_elevation(dt, location.latitude, location.longitude))

def test_SolarAzimuth():
    location_name = 'Jubail'
    
    dd = Astral()
    location=dd[location_name]
    print('Latitude: %f, Longitude: %f' % (location.latitude, location.longitude))

    dt = datetime.datetime.now(tz=location.tz)
    print('Date & time: %s' % dt)
    print('Date & time (UTC): %s' % dt.astimezone(pytz.utc))
    print('Azimuth: %.02f' % dd.solar_azimuth(dt, location.latitude, location.longitude))
    
def test_Moon():
    dd = Astral()
    tz = pytz.timezone('Europe/London')
    dd.moon_phase(datetime.date(2011,2,24), tz)
    
def test_Elevation():
    dd = Astral()
    c=dd['London']
    
    assert c.elevation == 24
