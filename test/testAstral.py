import datetime
import pytz
from astral import Astral, City

def testAstral():
    city_name = 'Jubail'
    
    dd = Astral()
    dd.solar_depression = 'civil'
    
    city = dd[city_name]
    
    print('Information for %s/%s\n' % (city_name, city.country))
    
    tz_name = city.tz_name
    print('Timezone: %s' % tz_name)
    
    loc_tz = pytz.timezone(tz_name)
    print('Latitude: %.02f; Longitude: %.02f\n' % (city.latitude, city.longitude))
    
    sun = city.sun()
    print('Dawn:     %s' % str(sun['dawn']))
    print('Sunrise:  %s' % str(sun['sunrise']))
    print('Noon:     %s' % str(sun['noon']))
    print('Sunset:   %s' % str(sun['sunset']))
    print('Dusk:     %s' % str(sun['dusk']))
    
    rahukaalam = city.rahukaalam()
    print('\nRahukaalam')
    print('Start:   %s' % str(rahukaalam['start']))
    print('End:     %s' % str(rahukaalam['end']))
    
    sunrise = city.sunrise(local=True)
    print('\nSunrise: %s' % str(sunrise))
    
    assert sunrise == sun['sunrise']

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
    
