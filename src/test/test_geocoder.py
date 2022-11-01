# -*- coding: utf-8 -*-
from functools import reduce
from typing import List

try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo

from pytest import approx, raises  # type: ignore

import astral.geocoder
from astral import LocationInfo
from astral.geocoder import LocationDatabase


def location_count(name: str, locations: List[LocationInfo]):
    return len(list(filter(lambda item: item.name == name, locations)))


def db_location_count(db: LocationDatabase) -> int:  # type: ignore
    """Returns the count of the locations currently in the database"""
    return reduce(lambda count, group: count + len(group), db.values(), 0)


class TestDatabase:
    """Test database access functions"""

    def test_all_locations(self, test_database: astral.geocoder.LocationDatabase):
        for loc in astral.geocoder.all_locations(test_database):
            assert loc.name

        location_list = astral.geocoder.all_locations(test_database)
        all_locations = list(location_list)
        assert location_count("London", all_locations) == 1
        assert location_count("Abu Dhabi", all_locations) == 2

    def test_lookup(self, test_database: astral.geocoder.LocationDatabase):
        loc = astral.geocoder.lookup("London", test_database)
        assert isinstance(loc, LocationInfo)
        assert loc.name == "London"
        assert loc.region == "England"
        assert loc.latitude == approx(51.4733, abs=0.001)
        assert loc.longitude == approx(-0.0008333, abs=0.000001)
        tz = zoneinfo.ZoneInfo("Europe/London")  # type: ignore
        tzl = zoneinfo.ZoneInfo(loc.timezone)  # type: ignore
        assert tz == tzl

    def test_city_in_db(self, test_database: astral.geocoder.LocationDatabase):
        astral.geocoder.lookup("london", test_database)

    def test_group_in_db(self, test_database: astral.geocoder.LocationDatabase):
        astral.geocoder.lookup("africa", test_database)

    def test_location_not_in_db(self, test_database: astral.geocoder.LocationDatabase):
        with raises(KeyError):
            astral.geocoder.lookup("Nowhere", test_database)

    def test_group_not_in_db(self, test_database: astral.geocoder.LocationDatabase):
        with raises(KeyError):
            astral.geocoder.group("wallyland", test_database)

    def test_lookup_city_and_region(
        self, test_database: astral.geocoder.LocationDatabase
    ):
        city_name = "Birmingham,England"

        city = astral.geocoder.lookup(city_name, test_database)
        assert isinstance(city, LocationInfo)
        assert city.name == "Birmingham"
        assert city.region == "England"

    def test_country_with_multiple_entries_no_country(
        self, test_database: astral.geocoder.LocationDatabase
    ):
        city = astral.geocoder.lookup("Abu Dhabi", test_database)
        assert isinstance(city, LocationInfo)
        assert city.name == "Abu Dhabi"

    def test_country_with_multiple_entries_with_country(
        self, test_database: astral.geocoder.LocationDatabase
    ):
        """Test for fix made due to bug report from Klaus Alexander Seistrup"""

        city = astral.geocoder.lookup("Abu Dhabi,United Arab Emirates", test_database)
        assert isinstance(city, LocationInfo)
        assert city.name == "Abu Dhabi"

        city = astral.geocoder.lookup("Abu Dhabi,UAE", test_database)
        assert isinstance(city, LocationInfo)
        assert city.name == "Abu Dhabi"


class TestBugReports:
    """Test for bug report fixes"""

    def test_Adelaide(self, test_database: astral.geocoder.LocationDatabase):
        """Test for fix made due to bug report from Klaus Alexander Seistrup"""

        astral.geocoder.lookup("Adelaide", test_database)

    def test_CandianCities(self, test_database: astral.geocoder.LocationDatabase):
        astral.geocoder.lookup("Fredericton", test_database)


class TestDatabaseAddLocations:
    """Test adding locations to database"""

    def test_newline_at_end(self, test_database: astral.geocoder.LocationDatabase):
        count = db_location_count(test_database)
        astral.geocoder.add_locations(
            "A Place,A Region,Asia/Nicosia,35°10'N,33°25'E,162.0\n", test_database
        )
        assert db_location_count(test_database) == count + 1

    def test_from_list_of_strings(
        self, test_database: astral.geocoder.LocationDatabase
    ):
        count = db_location_count(test_database)
        astral.geocoder.add_locations(
            [
                "A Place,A Region,Asia/Nicosia,35°10'N,33°25'E,162.0",
                "Another Place,Somewhere else,Asia/Nicosia,35°10'N,33°25'E,162.0",
            ],
            test_database,
        )
        assert db_location_count(test_database) == count + 2

    def test_from_list_of_lists(self, test_database: astral.geocoder.LocationDatabase):
        count = db_location_count(test_database)
        astral.geocoder.add_locations(
            [
                ["A Place", "A Region", "Asia/Nicosia", "35°10'N", "33°25'E", "162.0"],
                [
                    "Another Place",
                    "Somewhere else",
                    "Asia/Nicosia",
                    "35°10'N",
                    "33°25'E",
                    "162.0",
                ],
            ],
            test_database,
        )
        assert db_location_count(test_database) == count + 2


def test_SanitizeKey():
    assert astral.geocoder._sanitize_key("Los Angeles") == "los_angeles"  # type: ignore
