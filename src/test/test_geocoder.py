# -*- coding: utf-8 -*-
import pytz
from pytest import raises, approx

import astral.geocoder

def location_count(name, locations):
    return len(list(filter(lambda item: item.name == name, locations)))


class TestDatabase:
    """Test database access functions"""

    def test_all_locations(self, astral_database):
        for loc in astral.geocoder.all_locations(astral_database):
            assert loc.name

        location_list = astral.geocoder.all_locations(astral_database)
        all_locations = list(location_list)
        assert location_count("London", all_locations) == 1
        assert location_count("Abu Dhabi", all_locations) == 2

    def test_lookup(self, astral_database):
        loc = astral.geocoder.lookup("London", astral_database)
        assert loc.name == "London"
        assert loc.region == "England"
        assert approx(loc.latitude, 51.5)
        assert approx(loc.longitude, -0.166)
        tz = pytz.timezone("Europe/London")
        tzl = pytz.timezone(loc.timezone)
        assert tz == tzl
        assert loc.elevation == 24

    def test_city_in_db(self, astral_database):
        astral.geocoder.lookup("london", astral_database)

    def test_group_in_db(self, astral_database):
        astral.geocoder.lookup("africa", astral_database)

    def test_location_not_in_db(self, astral_database):
        with raises(KeyError):
            astral.geocoder.lookup("Nowhere", astral_database)

    def test_group_not_in_db(self, astral_database):
        with raises(KeyError):
            astral.geocoder.group("wallyland", astral_database)

    def test_lookup_city_and_region(self, astral_database):
        city_name = "Birmingham,England"

        city = astral.geocoder.lookup(city_name, astral_database)
        assert city.name == "Birmingham"
        assert city.region == "England"

    def test_country_with_multiple_entries_no_country(self, astral_database):
        city = astral.geocoder.lookup("Abu Dhabi", astral_database)
        assert city.name == "Abu Dhabi"

    def test_country_with_multiple_entries_with_country(self, astral_database):
        """Test for fix made due to bug report from Klaus Alexander Seistrup"""

        city = astral.geocoder.lookup("Abu Dhabi,United Arab Emirates", astral_database)
        assert city.name == "Abu Dhabi"

        city = astral.geocoder.lookup("Abu Dhabi,UAE", astral_database)
        assert city.name == "Abu Dhabi"


class TestBugReports:
    """Test for bug report fixes"""

    def test_Adelaide(self, astral_database):
        """Test for fix made due to bug report from Klaus Alexander Seistrup"""

        astral.geocoder.lookup("Adelaide", astral_database)

    def test_CandianCities(self, astral_database):
        city = astral.geocoder.lookup("Fredericton", astral_database)
        assert city.elevation == 8


class TestDatabaseAddLocations:
    """Test adding locations to database"""

    def test_newline_at_end(self, astral_database):
        count = astral.geocoder._location_count(astral_database)
        astral.geocoder.add_locations(
            "A Place,A Region,Asia/Nicosia,35°10'N,33°25'E,162.0\n", astral_database
        )
        assert astral.geocoder._location_count(astral_database) == count + 1

    def test_from_list_of_strings(self, astral_database):
        count = astral.geocoder._location_count(astral_database)
        astral.geocoder.add_locations(
            [
                "A Place,A Region,Asia/Nicosia,35°10'N,33°25'E,162.0",
                "Another Place,Somewhere else,Asia/Nicosia,35°10'N,33°25'E,162.0",
            ],
            astral_database,
        )
        assert astral.geocoder._location_count(astral_database) == count + 2

    def test_from_list_of_lists(self, astral_database):
        count = astral.geocoder._location_count(astral_database)
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
            astral_database,
        )
        assert astral.geocoder._location_count(astral_database) == count + 2


def test_SanitizeKey():
    assert astral.geocoder._sanitize_key("Los Angeles") == "los_angeles"
