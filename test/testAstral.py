from nose.tools import raises

import datetime
import pytz
from astral import Astral, City
    
@raises(KeyError)
def testAstralBadCityName():
    dd = Astral()
    c = dd['wally']    

def testAstralCityName():
    dd = Astral()
    c = dd['London']
    assert c.name == 'London'    

@raises(TypeError)
def testAstralAssign():
    dd = Astral()
    dd['London'] = 'wally'    


def testAstral():
    city_name = 'Jubail'
    
    dd = Astral()
    dd.solar_depression = 'civil'
    
    city = dd[city_name]
    
    print('Information for %s/%s\n' % (city_name, city.country))
    
    timezone = city.timezone
    print('Timezone: %s' % timezone)
    
    loc_tz = pytz.timezone(timezone)
    print('Latitude: %.02f; Longitude: %.02f\n' % (city.latitude, city.longitude))
    
    sun = city.sun()
    sunrise = city.sunrise(local=True)
    assert sunrise == sun['sunrise']

    rahukaalam = city.rahukaalam()

def testElevation():
    city_name = 'Jubail'
    
    dd = Astral()
    city=dd[city_name]

    dt = datetime.datetime.now(tz=city.tz)
    print('Date & time: %s' % dt)
    print('Date & time (UTC): %s' % dt.astimezone(pytz.utc))
    print('Elevation: %.02f' % dd.solar_elevation(dt, city.latitude, city.longitude))

def testAzimuth():
    city_name = 'Jubail'
    
    dd = Astral()
    city=dd[city_name]
    print('Latitude: %f, Longitude: %f' % (city.latitude, city.longitude))

    dt = datetime.datetime.now(tz=city.tz)
    print('Date & time: %s' % dt)
    print('Date & time (UTC): %s' % dt.astimezone(pytz.utc))
    print('Azimuth: %.02f' % dd.solar_azimuth(dt, city.latitude, city.longitude))
    
if __name__ == "__main__":
    testElevation()
    testAzimuth()
    
