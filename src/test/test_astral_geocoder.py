# -*- coding: utf-8 -*-
import pytz
from pytest import raises, approx

import astral.geocoder


def test_AllLocations(astral_database):
    for loc in astral.geocoder.all_locations(astral_database):
        assert loc.name

    location_list = astral.geocoder.all_locations(astral_database)
    assert len(list(filter(lambda item: item.name == "London", location_list))) == 1


def test_Lookup(astral_database):
    loc = astral.geocoder.lookup("London", astral_database)
    assert loc.name == "London"
    assert loc.region == "England"
    assert approx(loc.latitude, 51.5)
    assert approx(loc.longitude, -0.166)
    tz = pytz.timezone("Europe/London")
    tzl = pytz.timezone(loc.timezone)
    assert tz == tzl
    assert loc.elevation == 24


def test_UnknownLocation(astral_database):
    with raises(KeyError):
        astral.geocoder.lookup("Nowhere", astral_database)


def test_Group(astral_database):
    astral.geocoder.group("europe", astral_database)


def test_UnknownGroup(astral_database):
    with raises(KeyError):
        astral.geocoder.group("wallyland", astral_database)


def test_CityContainment(astral_database):
    astral.geocoder.lookup("london", astral_database)


def test_GroupContainment(astral_database):
    astral.geocoder.lookup("africa", astral_database)


def test_CityCountry(astral_database):
    city_name = "Birmingham,England"

    city = astral.geocoder.lookup(city_name, astral_database)
    assert city.name == "Birmingham"
    assert city.region == "England"


def test_MultiCountry(astral_database):
    city = astral.geocoder.lookup("Abu Dhabi", astral_database)
    assert city.name == "Abu Dhabi"


def test_MultiCountryWithCountry(astral_database):
    """Test for fix made due to bug report from Klaus Alexander Seistrup"""

    city = astral.geocoder.lookup("Abu Dhabi,United Arab Emirates", astral_database)
    assert city.name == "Abu Dhabi"

    city = astral.geocoder.lookup("Abu Dhabi,UAE", astral_database)
    assert city.name == "Abu Dhabi"


def test_Adelaide(astral_database):
    """Test for fix made due to bug report from Klaus Alexander Seistrup"""

    astral.geocoder.lookup("Adelaide", astral_database)


def test_CandianCities(astral_database):
    city = astral.geocoder.lookup("Fredericton", astral_database)
    assert city.elevation == 8


def test_AddLocation_NewlineAtEnd(astral_database):
    count = astral.geocoder._location_count(astral_database)
    astral.geocoder.add_locations(
        "A Place,A Region,Asia/Nicosia,35°10'N,33°25'E,162.0\n", astral_database
    )
    assert astral.geocoder._location_count(astral_database) == count + 1


def test_AddLocation_FromListOfStrings(astral_database):
    count = astral.geocoder._location_count(astral_database)
    astral.geocoder.add_locations(
        [
            "A Place,A Region,Asia/Nicosia,35°10'N,33°25'E,162.0",
            "Another Place,Somewhere else,Asia/Nicosia,35°10'N,33°25'E,162.0",
        ],
        astral_database,
    )
    assert astral.geocoder._location_count(astral_database) == count + 2


def test_AddLocation_FromListOfLists(astral_database):
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
