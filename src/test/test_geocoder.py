# -*- coding: utf-8 -*-
import pytz
from pytest import raises, approx

import astral.geocoder


def location_count(name, locations):
    return len(list(filter(lambda item: item.name == name, locations)))


class TestDatabase:
    """Test database access functions"""

    def test_all_locations(self, test_database):
        for loc in astral.geocoder.all_locations(test_database):
            assert loc.name

        location_list = astral.geocoder.all_locations(test_database)
        all_locations = list(location_list)
        assert location_count("London", all_locations) == 1
        assert location_count("Abu Dhabi", all_locations) == 2

    def test_lookup(self, test_database):
        loc = astral.geocoder.lookup("London", test_database)
        assert loc.name == "London"
        assert loc.region == "England"
        assert loc.latitude == approx(51.4733, abs=0.001)
        assert loc.longitude == approx(-0.0008333, abs=0.000001)
        tz = pytz.timezone("Europe/London")
        tzl = pytz.timezone(loc.timezone)
        assert tz == tzl

    def test_city_in_db(self, test_database):
        astral.geocoder.lookup("london", test_database)

    def test_group_in_db(self, test_database):
        astral.geocoder.lookup("africa", test_database)

    def test_location_not_in_db(self, test_database):
        with raises(KeyError):
            astral.geocoder.lookup("Nowhere", test_database)

    def test_group_not_in_db(self, test_database):
        with raises(KeyError):
            astral.geocoder.group("wallyland", test_database)

    def test_lookup_city_and_region(self, test_database):
        city_name = "Birmingham,England"

        city = astral.geocoder.lookup(city_name, test_database)
        assert city.name == "Birmingham"
        assert city.region == "England"

    def test_country_with_multiple_entries_no_country(self, test_database):
        city = astral.geocoder.lookup("Abu Dhabi", test_database)
        assert city.name == "Abu Dhabi"

    def test_country_with_multiple_entries_with_country(self, test_database):
        """Test for fix made due to bug report from Klaus Alexander Seistrup"""

        city = astral.geocoder.lookup("Abu Dhabi,United Arab Emirates", test_database)
        assert city.name == "Abu Dhabi"

        city = astral.geocoder.lookup("Abu Dhabi,UAE", test_database)
        assert city.name == "Abu Dhabi"


class TestBugReports:
    """Test for bug report fixes"""

    def test_Adelaide(self, test_database):
        """Test for fix made due to bug report from Klaus Alexander Seistrup"""

        astral.geocoder.lookup("Adelaide", test_database)

    def test_CandianCities(self, test_database):
        astral.geocoder.lookup("Fredericton", test_database)


class TestDatabaseAddLocations:
    """Test adding locations to database"""

    def test_newline_at_end(self, test_database):
        count = astral.geocoder._location_count(test_database)
        astral.geocoder.add_locations(
            "A Place,A Region,Asia/Nicosia,35°10'N,33°25'E,162.0\n", test_database
        )
        assert astral.geocoder._location_count(test_database) == count + 1

    def test_from_list_of_strings(self, test_database):
        count = astral.geocoder._location_count(test_database)
        astral.geocoder.add_locations(
            [
                "A Place,A Region,Asia/Nicosia,35°10'N,33°25'E,162.0",
                "Another Place,Somewhere else,Asia/Nicosia,35°10'N,33°25'E,162.0",
            ],
            test_database,
        )
        assert astral.geocoder._location_count(test_database) == count + 2

    def test_from_list_of_lists(self, test_database):
        count = astral.geocoder._location_count(test_database)
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
        assert astral.geocoder._location_count(test_database) == count + 2


def test_SanitizeKey():
    assert astral.geocoder._sanitize_key("Los Angeles") == "los_angeles"
