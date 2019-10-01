# -*- coding: utf-8 -*-
from almost_equal import datetime_almost_equal
import freezegun
import pytest

from astral import AstralError, LocationInfo
from astral.location import Location
import dataclasses
import datetime
import pytz


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


def test_Location_Info(london, london_info):
    assert london_info == london.info


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
    c.noon()


def test_Location_SolarNoonUTC():
    c = Location()
    c.noon(local=False)


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
        dt = new_delhi.time_at_elevation(28, day)
        assert datetime_almost_equal(dt, cdt, seconds=600)


def test_Location_SolarDepression():
    c = Location(LocationInfo("Heidelberg", "Germany", "Europe/Berlin", 49.412, -8.71))
    c.solar_depression = "nautical"
    assert c.solar_depression == 12

    c.solar_depression = 18
    assert c.solar_depression == 18


def test_Location_BadSolarDepression():
    loc = Location()
    with pytest.raises(KeyError):
        loc.solar_depression = "uncivil"


def test_Location_Moon():
    d = datetime.date(2017, 12, 1)
    c = Location()
    assert c.moon_phase(date=d) == 11


@freezegun.freeze_time("2015-12-01")
def test_Location_MoonNoDate():
    c = Location()
    assert c.moon_phase() == 19


def test_Location_TzError():
    with pytest.raises(AttributeError):
        c = Location()
        c.tz = 1


def test_Location_Equality():
    c1 = Location()
    c2 = Location()
    assert c1 == c2


def test_LocationEquality_NotEqual(london_info):
    location1 = Location(london_info)
    location2 = Location(london_info)
    location2.elevation = 23.0

    assert location2 != location1


def test_LocationEquality_NotALocation(london_info):
    location = Location(london_info)

    class NotALocation():
        _location_info = london_info

    assert NotALocation() != location


def test_Location_SetLatitudeFloat():
    loc = Location()
    loc.latitude = 34.0
    assert loc.latitude == 34.0


def test_Location_SetLatitudeString():
    loc = Location()
    loc.latitude = "24°28'N"

    assert pytest.approx(loc.latitude, 24.46666666666666)


def test_Location_SetLongitudeFloat():
    loc = Location()
    loc.longitude = 24.0
    assert loc.longitude == 24.0


def test_Location_SetLongitudeString():
    loc = Location()
    loc.longitude = "24°28'S"

    assert pytest.approx(loc.longitude, -24.46666666666666)


def test_Location_SetBadLongitudeString():
    loc = Location()
    with pytest.raises(ValueError):
        loc.longitude = "wibble"


def test_Location_BadTzinfo():
    loc = Location()
    loc._location_info = dataclasses.replace(loc._location_info, timezone="Bad/Timezone")

    with pytest.raises(AstralError):
        loc.tzinfo
