# -*- coding: utf-8 -*-
from nose.tools import raises

import datetime
import pytz
from astral import Astral, City
    
@raises(KeyError)
def test_AstralBadCityName():
    dd = Astral()
    c = dd['wally']    

def test_AstralCityName():
    dd = Astral()
    c = dd['London']
    assert c.name == 'London'    

@raises(TypeError)
def test_AstralAssign():
    dd = Astral()
    dd['London'] = 'wally'    


def test_Astral():
    city_name = 'Jubail'
    
    dd = Astral()
    dd.solar_depression = 'civil'
    
    city = dd[city_name]
    assert city.timezone == 'Asia/Riyadh'
    
    print('Information for %s/%s\n' % (city_name, city.country))
    
    timezone = city.timezone
    print('Timezone: %s' % timezone)
    
    loc_tz = pytz.timezone(timezone)
    print('Latitude: %.02f; Longitude: %.02f\n' % (city.latitude, city.longitude))
    
    sun = city.sun()
    sunrise = city.sunrise(local=True)
    assert sunrise == sun['sunrise']

    rahukaalam = city.rahukaalam()

def test_Elevation():
    city_name = 'Jubail'
    
    dd = Astral()
    city=dd[city_name]

    dt = datetime.datetime.now(tz=city.tz)
    print('Date & time: %s' % dt)
    print('Date & time (UTC): %s' % dt.astimezone(pytz.utc))
    print('Elevation: %.02f' % dd.solar_elevation(dt, city.latitude, city.longitude))

def test_Azimuth():
    city_name = 'Jubail'
    
    dd = Astral()
    city=dd[city_name]
    print('Latitude: %f, Longitude: %f' % (city.latitude, city.longitude))

    dt = datetime.datetime.now(tz=city.tz)
    print('Date & time: %s' % dt)
    print('Date & time (UTC): %s' % dt.astimezone(pytz.utc))
    print('Azimuth: %.02f' % dd.solar_azimuth(dt, city.latitude, city.longitude))
    
def test_Moon():
    dd = Astral()
    dd.moon_phase(datetime.date(2011,2,24))
    
if __name__ == "__main__":
    test_Astral()
    test_Elevation()
    test_Azimuth()
    test_Moon()
