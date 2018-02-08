# -*- coding: utf-8 -*-
import pytest

import pytz
import datetime
import math
from astral import Astral


def float_almost_equal(value1, value2, diff=0.5):
    return abs(value1 - value2) <= diff


def test_AstralBadLocationName():
    with pytest.raises(KeyError):
        dd = Astral()
        _c = dd['wally']


def test_AstralLocationName():
    dd = Astral()
    c = dd['London']
    assert c.name == 'London'


def test_AstralAssign():
    with pytest.raises(TypeError):
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


def test_Astral_SolarNoon():
    dd = Astral()
    dt = datetime.datetime(2017, 2, 10)

    noon = dd.solar_noon_utc(dt, 49.65)
    assert noon.hour == 8
    assert noon.minute == 55
    assert noon.second == 37


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


def test_Astral_SolarZenith():
    dd = Astral()
    dt = datetime.datetime(2015, 2, 3, 9, 0, 0, tzinfo=pytz.UTC)

    zenith = dd.solar_zenith(dt, 51.5, -0.12)
    assert float_almost_equal(zenith, 90.0 - 9.97, 0.1)


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


def test_Astral_JulianDay_Date():
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


def test_Astral_JulianDay_DateTime():
    a = Astral()

    dt = datetime.datetime(2015, 1, 1, 1, 36, 0)
    jd = a._julianday(dt)
    assert float_almost_equal(jd, 2457023.57, 0.1)

    dt = datetime.datetime(2015, 1, 1, 15, 12, 0)
    jd = a._julianday(dt)
    assert float_almost_equal(jd, 2457024.13, 0.1)


def test_Astral_JulianDay_DateTimeZone():
    a = Astral()

    dt = datetime.datetime(2015, 1, 1, 1, 36, 0)
    jd = a._julianday(dt, 1)
    assert float_almost_equal(jd, 2457023.51, 0.1)

    dt = datetime.datetime(2015, 10, 10, 1, 36, 0)
    jd = a._julianday(dt, 5)
    assert float_almost_equal(jd, 2457305.36, 0.1)


def test_GeomMeanLongSun():
    a = Astral()

    dt = datetime.datetime(2015, 10, 10, 1, 36, 0)
    jc = a._jday_to_jcentury(a._julianday(dt, 5))
    geom = a._geom_mean_long_sun(jc)
    assert float_almost_equal(geom, 198.1484524, 0.1)

    dt = datetime.datetime(2015, 1, 1, 1, 36, 0)
    jc = a._jday_to_jcentury(a._julianday(dt, -4))
    geom = a._geom_mean_long_sun(jc)
    assert float_almost_equal(geom, 280.5655139, 0.1)


def test_GeomMeanAnomalySun():
    a = Astral()

    dt = datetime.date(2015, 10, 10)
    jc = a._jday_to_jcentury(a._julianday(dt, -4))
    geom = a._geom_mean_anomaly_sun(jc)
    assert float_almost_equal(geom, 6035.243796, 0.1)


def test_EccentrilocationEarthOrbit():
    a = Astral()

    dt = datetime.date(2015, 10, 10)
    jc = a._jday_to_jcentury(a._julianday(dt, -4))
    ecc = a._eccentrilocation_earth_orbit(jc)
    assert float_almost_equal(ecc, 0.016702001, 0.1)


def test_SunEqOfCenter():
    a = Astral()

    dt = datetime.date(2015, 10, 10)
    jc = a._jday_to_jcentury(a._julianday(dt, -4))
    eoc = a._sun_eq_of_center(jc)
    assert float_almost_equal(eoc, -1.909033734, 0.1)


def test_SunTrueLong():
    a = Astral()

    dt = datetime.date(2015, 10, 10)
    jc = a._jday_to_jcentury(a._julianday(dt, -4))
    true_long = a._sun_true_long(jc)
    assert float_almost_equal(true_long, 196.6090364, 0.1)


def test_SunTrueAnomoly():
    a = Astral()

    dt = datetime.date(2015, 10, 10)
    jc = a._jday_to_jcentury(a._julianday(dt, -4))
    true_long = a._sun_true_anomoly(jc)
    assert float_almost_equal(true_long, 6033.400469, 0.1)


def test_SunRadVector():
    a = Astral()

    dt = datetime.date(2015, 10, 10)
    jc = a._jday_to_jcentury(a._julianday(dt, -4))
    rad_vector = a._sun_rad_vector(jc)
    assert float_almost_equal(rad_vector, 0.998732645, 0.1)


def test_SunApparentLong():
    a = Astral()

    dt = datetime.date(2015, 10, 10)
    jc = a._jday_to_jcentury(a._julianday(dt, -4))
    apparent_long = a._sun_apparent_long(jc)
    assert float_almost_equal(apparent_long, 196.6033454, 0.1)


def test_MeanObliquityOfEcliptic():
    a = Astral()

    dt = datetime.date(2015, 10, 10)
    jc = a._jday_to_jcentury(a._julianday(dt, -4))
    mean_obliquity = a._mean_obliquity_of_ecliptic(jc)
    assert float_almost_equal(mean_obliquity, 23.43724009, 0.1)


def test_ObliquityCorrection():
    a = Astral()

    dt = datetime.datetime(2015, 10, 10, 1, 36, 0)
    jc = a._jday_to_jcentury(a._julianday(dt, -4))
    obliquity_correction = a._obliquity_correction(jc)
    assert float_almost_equal(obliquity_correction, 23.43468009, 0.0001)


def test_SunRightAscension():
    a = Astral()

    dt = datetime.date(2015, 10, 10)
    jc = a._jday_to_jcentury(a._julianday(dt, -4))
    rt_ascension = a._sun_rt_ascension(jc)
    assert float_almost_equal(rt_ascension, -164.7605748, 0.001)


def test_SunDeclination():
    a = Astral()

    dt = datetime.datetime(2015, 10, 10, 1, 36, 0)
    jc = a._jday_to_jcentury(a._julianday(dt, -4))
    declination = a._sun_declination(jc)
    assert float_almost_equal(declination, -6.525273018, 0.0001)


def test_VarY():
    a = Astral()

    dt = datetime.datetime(2015, 10, 10, 0, 54, 0)
    jc = a._jday_to_jcentury(a._julianday(dt, -4))
    y = a._var_y(jc)
    assert float_almost_equal(y, 0.043017118, 0.0001)


def test_EquationOfTime():
    a = Astral()

    dt = datetime.datetime(2015, 10, 10, 0, 54, 0)
    jc = a._jday_to_jcentury(a._julianday(dt, -4))
    etime = a._eq_of_time(jc)
    assert float_almost_equal(etime, 12.84030157, 0.0001)

    dt = datetime.datetime(2017, 1, 1, 2, 0, 0)
    jc = a._jday_to_jcentury(a._julianday(dt, 2))
    etime = a._eq_of_time(jc)
    assert float_almost_equal(etime, -3.438084536, 0.0001)


def test_SunriseHourAngle():
    a = Astral()

    dt = datetime.date(2015, 1, 1)
    jc = a._jday_to_jcentury(a._julianday(dt, 1))
    declination = a._sun_declination(jc)
    ha = math.degrees(a._hour_angle(52.169, declination, 90.833))
    assert float_almost_equal(ha, 58.6102679, 0.1)

@pytest.mark.parametrize("test", ["dawn_utc", "sunrise_utc", "sunset_utc", "dusk_utc"])
def test_UTC_BadDate(test):
    a = Astral()
    func = getattr(a, test)

    with pytest.raises(AttributeError):
        l = func('s', 1, -0.5)


@pytest.mark.parametrize("test", ["dawn_utc", "sunrise_utc", "sunset_utc", "dusk_utc"])
def test_UTC_BadLatitude(test):
    a = Astral()
    func = getattr(a, test)
    dt = datetime.date(2015, 1, 1)

    with pytest.raises(TypeError):
        l = func(dt, 1, 'a')


@pytest.mark.parametrize("test", ["dawn_utc", "sunrise_utc", "sunset_utc", "dusk_utc"])
def test_UTC_BadLongitude(test):
    a = Astral()
    func = getattr(a, test)
    dt = datetime.date(2015, 1, 1)

    with pytest.raises(TypeError):
        l = func(dt, 'a', 1)
