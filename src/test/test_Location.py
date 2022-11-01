# -*- coding: utf-8 -*-
import dataclasses
import datetime

try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo

import freezegun
import pytest
from almost_equal import datetime_almost_equal

from astral import LocationInfo
from astral.location import Location


class TestLocation:
    """Tests for the Location class"""

    def test_Name(self):
        """Test the default name and that the name is changeable"""
        c = Location()
        assert c.name == "Greenwich"
        c.name = "Köln"
        assert c.name == "Köln"

    def test_Region(self):
        """Test the default region and that the region is changeable"""
        c = Location()
        assert c.region == "England"
        c.region = "Australia"
        assert c.region == "Australia"

    def test_TimezoneName(self):
        """Test the default timezone and that the timezone is changeable"""
        c = Location()
        assert c.timezone == "Europe/London"
        c.name = "Asia/Riyadh"
        assert c.name == "Asia/Riyadh"

    def test_TimezoneNameBad(self):
        """Test that an exception is raised if an invalid timezone is specified"""
        c = Location()
        with pytest.raises(ValueError):
            c.timezone = "bad/timezone"

    def test_TimezoneLookup(self):
        """Test that tz refers to a timezone object"""
        c = Location()
        assert c.tz == zoneinfo.ZoneInfo("Europe/London")  # type: ignore
        c.timezone = "Europe/Stockholm"
        assert c.tz == zoneinfo.ZoneInfo("Europe/Stockholm")  # type: ignore

    def test_Info(self, london: Location, london_info: LocationInfo):
        assert london_info == london.info

    def test_Sun(self, london: Location):
        """Test Location's version of the sun calculation"""
        ldt = datetime.datetime(2015, 8, 1, 5, 23, 20, tzinfo=london.tz)
        sunrise = london.sun(datetime.date(2015, 8, 1))["sunrise"]
        assert datetime_almost_equal(sunrise, ldt)

    def test_Dawn(self, london: Location):
        """Test Location returns dawn times in the local timezone"""
        ldt = datetime.datetime(2015, 8, 1, 4, 41, 44, tzinfo=london.tz)
        dawn = london.dawn(datetime.date(2015, 8, 1))
        assert datetime_almost_equal(dawn, ldt)
        # assert dawn.tzinfo.zone == london.tzinfo.zone

    def test_DawnUTC(self, london: Location):
        """Test Location returns dawn times in the UTC timezone"""
        udt = datetime.datetime(2015, 8, 1, 3, 41, 44, tzinfo=datetime.timezone.utc)
        dawn = london.dawn(datetime.date(2015, 8, 1), local=False)
        assert datetime_almost_equal(dawn, udt)
        # assert dawn.tzinfo.zone == datetime.timezone.utc.zone

    def test_Sunrise(self, london: Location):
        ldt = datetime.datetime(2015, 8, 1, 5, 23, 20, tzinfo=london.tz)
        sunrise = london.sunrise(datetime.date(2015, 8, 1))
        assert datetime_almost_equal(sunrise, ldt)
        # assert sunrise.tzinfo.zone == london.tzinfo.zone

    def test_SunriseUTC(self, london: Location):
        udt = datetime.datetime(2015, 8, 1, 4, 23, 20, tzinfo=datetime.timezone.utc)
        sunrise = london.sunrise(datetime.date(2015, 8, 1), local=False)
        assert datetime_almost_equal(sunrise, udt)
        # assert sunrise.tzinfo.zone == datetime.timezone.utc.zone

    def test_SolarNoon(self, london: Location):
        ldt = datetime.datetime(2015, 8, 1, 13, 6, 53, tzinfo=london.tz)
        noon = london.noon(datetime.date(2015, 8, 1))
        assert datetime_almost_equal(noon, ldt)
        # assert noon.tzinfo.zone == london.tzinfo.zone

    def test_SolarNoonUTC(self, london: Location):
        udt = datetime.datetime(2015, 8, 1, 12, 6, 53, tzinfo=datetime.timezone.utc)
        noon = london.noon(datetime.date(2015, 8, 1), local=False)
        assert datetime_almost_equal(noon, udt)
        # assert noon.tzinfo.zone == datetime.timezone.utc.zone

    def test_Dusk(self, london: Location):
        ldt = datetime.datetime(2015, 12, 1, 16, 35, 11, tzinfo=london.tz)
        dusk = london.dusk(datetime.date(2015, 12, 1))
        assert datetime_almost_equal(dusk, ldt)
        # assert dusk.tzinfo.zone == london.tzinfo.zone

    def test_DuskUTC(self, london: Location):
        udt = datetime.datetime(2015, 12, 1, 16, 35, 11, tzinfo=datetime.timezone.utc)
        dusk = london.dusk(datetime.date(2015, 12, 1), local=False)
        assert datetime_almost_equal(dusk, udt)
        # assert dusk.tzinfo.zone == datetime.timezone.utc.zone

    def test_Sunset(self, london: Location):
        ldt = datetime.datetime(2015, 12, 1, 15, 55, 29, tzinfo=london.tz)
        sunset = london.sunset(datetime.date(2015, 12, 1))
        assert datetime_almost_equal(sunset, ldt)
        # assert sunset.tzinfo.zone == london.tzinfo.zone

    def test_SunsetUTC(self, london: Location):
        udt = datetime.datetime(2015, 12, 1, 15, 55, 29, tzinfo=datetime.timezone.utc)
        sunset = london.sunset(datetime.date(2015, 12, 1), local=False)
        assert datetime_almost_equal(sunset, udt)
        # assert sunset.tzinfo.zone == datetime.timezone.utc.zone

    def test_SolarElevation(self, riyadh: Location):
        dt = datetime.datetime(2015, 12, 14, 8, 0, 0, tzinfo=riyadh.tz)
        elevation = riyadh.solar_elevation(dt)
        assert abs(elevation - 17) < 0.5

    def test_SolarAzimuth(self, riyadh: Location):
        dt = datetime.datetime(2015, 12, 14, 8, 0, 0, tzinfo=riyadh.tz)
        azimuth = riyadh.solar_azimuth(dt)
        assert abs(azimuth - 126) < 0.5

    def test_TimeAtAltitude(self, new_delhi: Location):
        test_data = {datetime.date(2016, 1, 5): datetime.datetime(2016, 1, 5, 10, 0)}

        for day, cdt in test_data.items():
            cdt = cdt.replace(tzinfo=new_delhi.tz)
            dt = new_delhi.time_at_elevation(28, day)
            assert datetime_almost_equal(dt, cdt, seconds=600)

    def test_SolarDepression(self):
        c = Location(
            LocationInfo("Heidelberg", "Germany", "Europe/Berlin", 49.412, -8.71)
        )
        c.solar_depression = "nautical"
        assert c.solar_depression == 12

        c.solar_depression = 18
        assert c.solar_depression == 18

    def test_BadSolarDepression(self):
        loc = Location()
        with pytest.raises(KeyError):
            loc.solar_depression = "uncivil"

    def test_Moon(self):
        d = datetime.date(2017, 12, 1)
        c = Location()
        assert c.moon_phase(date=d) == pytest.approx(11.62, abs=0.01)  # type: ignore

    @freezegun.freeze_time("2015-12-01")
    def test_MoonNoDate(self):
        c = Location()
        assert c.moon_phase() == pytest.approx(19.47, abs=0.01)  # type: ignore

    def test_TzError(self):
        with pytest.raises(AttributeError):
            c = Location()
            c.tz = 1  # type: ignore

    def test_Equality(self):
        c1 = Location()
        c2 = Location()
        assert c1 == c2

    def test_LocationEquality_NotEqual(self, london_info: LocationInfo):
        location1 = Location(london_info)
        location2 = Location(london_info)
        location2.latitude = 23.0

        assert location2 != location1

    def test_LocationEquality_NotALocation(self, london_info: LocationInfo):
        location = Location(london_info)

        class NotALocation:
            _location_info = london_info

        assert NotALocation() != location

    def test_SetLatitudeFloat(self):
        loc = Location()
        loc.latitude = 34.0
        assert loc.latitude == 34.0

    def test_SetLatitudeString(self):
        loc = Location()
        loc.latitude = "24°28'N"

        assert loc.latitude == pytest.approx(24.46666666666666)  # type: ignore

    def test_SetLongitudeFloat(self):
        loc = Location()
        loc.longitude = 24.0
        assert loc.longitude == 24.0

    def test_SetLongitudeString(self):
        loc = Location()
        loc.longitude = "24°28'S"

        assert loc.longitude == pytest.approx(-24.46666666666666)  # type: ignore

    def test_SetBadLongitudeString(self):
        loc = Location()
        with pytest.raises(ValueError):
            loc.longitude = "wibble"

    def test_BadTzinfo(self):
        loc = Location()
        loc._location_info = dataclasses.replace(  # type: ignore
            loc._location_info, timezone="Bad/Timezone"  # type: ignore
        )

        with pytest.raises(ValueError):
            loc.tzinfo
