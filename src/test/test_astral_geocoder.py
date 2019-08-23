# -*- coding: utf-8 -*-
import pytz
from pytest import raises, approx

import astral.geocoder


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


def test_Group():
    db = astral.geocoder.Geocoder()
    db.europe


def test_UnknownGroup():
    with raises(AttributeError):
        db = astral.geocoder.Geocoder()
        db.wallyland


def test_CityContainment():
    db = astral.geocoder.Geocoder()
    assert "london" in db


def test_GroupContainment():
    db = astral.geocoder.Geocoder()
    assert "africa" in db


def test_CityCountry():
    city_name = "Birmingham,England"

    db = astral.geocoder.Geocoder()
    city = db[city_name]
    assert city.name == "Birmingham"
    assert city.region == "England"


def test_MultiCountry():
    db = astral.geocoder.Geocoder()
    city = db["Abu Dhabi"]
    assert city.name == "Abu Dhabi"


def test_MultiCountryWithCountry():
    """Test for fix made due to bug report from Klaus Alexander Seistrup"""

    db = astral.geocoder.Geocoder()
    city = db["Abu Dhabi,United Arab Emirates"]
    assert city.name == "Abu Dhabi"

    city = db["Abu Dhabi,UAE"]
    assert city.name == "Abu Dhabi"


def test_Adelaide():
    """Test for fix made due to bug report from Klaus Alexander Seistrup"""

    db = astral.geocoder.Geocoder()
    db["Adelaide"]


def test_CandianCities():
    db = astral.geocoder.Geocoder()

    city = db["Fredericton"]
    assert city.elevation == 8


def test_AllCities():
    db = astral.geocoder.Geocoder()
    locations = db.locations
    locations.sort()

    for city_name in locations:
        db[city_name]


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
