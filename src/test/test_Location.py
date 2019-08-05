# -*- coding: utf-8 -*-
import pytest

from astral import LocationInfo
from astral.location import Location
import datetime
import pytz


def datetime_almost_equal(datetime1, datetime2, seconds=60):
    dd = datetime1 - datetime2
    sd = (dd.days * 24 * 60 * 60) + dd.seconds
    return abs(sd) <= seconds


def test_Location_Name():
    c = Location()
    assert c.name == "Greenwich"
    c.name = "London"
    assert c.name == "London"
    c.name = "Köln"
    assert c.name == "Köln"


def test_Location_Country():
    c = Location()
    assert c.region == "England"
    c.region = "Australia"
    assert c.region == "Australia"


def test_Location_Elevation():
    c = Location()
    assert c.elevation == 24


def test_Location_TimezoneName():
    c = Location()
    assert c.timezone == "Europe/London"
    c.name = "Asia/Riyadh"
    assert c.name == "Asia/Riyadh"


def test_Location_TimezoneNameBad():
    c = Location()
    with pytest.raises(ValueError):
        c.timezone = "bad/timezone"


def test_Location_TimezoneLookup():
    c = Location()
    assert c.tz == pytz.timezone("Europe/London")
    c.timezone = "Europe/Stockholm"
    assert c.tz == pytz.timezone("Europe/Stockholm")


def test_Location_TimezoneLookupBad():
    c = Location()
    with pytest.raises(ValueError):
        c.timezone = "bad/timezone"


def test_Location_Sun():
    c = Location()
    c.sun()


def test_Location_Dawn():
    c = Location()
    c.dawn()


def test_Location_DawnUTC():
    c = Location()
    c.dawn(local=False)


def test_Location_Sunrise():
    c = Location()
    c.sunrise()


def test_Location_SunriseUTC():
    c = Location()
    c.sunrise(local=False)


def test_Location_SolarNoon():
    c = Location()
    c.solar_noon()


def test_Location_SolarNoonUTC():
    c = Location()
    c.solar_noon(local=False)


def test_Location_Dusk():
    c = Location()
    c.dusk()


def test_Location_DuskUTC():
    c = Location()
    c.dusk(local=False)


def test_Location_Sunset():
    c = Location()
    c.sunset()


def test_Location_SunsetUTC():
    c = Location()
    c.sunset(local=False)


def test_Location_SolarElevation(riyadh):
    dt = datetime.datetime(2015, 12, 14, 8, 0, 0)
    dt = riyadh.tz.localize(dt)
    elevation = riyadh.solar_elevation(dt)
    assert abs(elevation - 17) < 0.5


def test_Location_SolarAzimuth(riyadh):
    dt = datetime.datetime(2015, 12, 14, 8, 0, 0)
    dt = riyadh.tz.localize(dt)
    azimuth = riyadh.solar_azimuth(dt)
    assert abs(azimuth - 126) < 0.5


def test_Location_TimeAtAltitude(new_delhi):
    test_data = {datetime.date(2016, 1, 5): datetime.datetime(2016, 1, 5, 10, 0)}

    for day, cdt in test_data.items():
        cdt = new_delhi.tz.localize(cdt)
        dt = new_delhi.time_at_altitude(28, day)
        assert datetime_almost_equal(dt, cdt, seconds=600)


def test_Location_SolarDepression():
    c = Location(LocationInfo("Heidelberg", "Germany", "Europe/Berlin", 49.412, -8.71))
    c.solar_depression = "nautical"
    assert c.solar_depression == 12

    c.solar_depression = 18
    assert c.solar_depression == 18


def test_Location_Moon():
    d = datetime.date(2017, 12, 1)
    c = Location()
    assert c.moon_phase(date=d) == 11


def test_Location_TzError():
    with pytest.raises(AttributeError):
        c = Location()
        c.tz = 1


def test_Location_Equality():
    c1 = Location()
    c2 = Location()
    assert c1 == c2
