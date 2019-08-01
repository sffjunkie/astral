# -*- coding: utf-8 -*-
import pytz
from pytest import raises, approx

from astral.geocoder import Geocoder, lookup


def test_Lookup():
    l = lookup("London")
    assert l.name == "London"
    assert l.region == "England"
    assert approx(l.latitude, 51.5)
    assert approx(l.longitude, -0.166)
    tz = pytz.timezone("Europe/London")
    tzl = pytz.timezone(l.timezone)
    assert tz == tzl
    assert l.elevation == 24


def test_Group():
    db = Geocoder()
    _e = db.europe


def test_UnknownGroup():
    with raises(AttributeError):
        db = Geocoder()
        _e = db.wallyland


def test_CityContainment():
    db = Geocoder()
    assert "london" in db


def test_GroupContainment():
    db = Geocoder()
    assert "africa" in db


def test_CityCountry():
    city_name = "Birmingham,England"

    db = Geocoder()
    city = db[city_name]
    assert city.name == "Birmingham"
    assert city.region == "England"


def test_MultiCountry():
    db = Geocoder()
    city = db["Abu Dhabi"]
    assert city.name == "Abu Dhabi"


def test_MultiCountryWithCountry():
    """Test for fix made due to bug report from Klaus Alexander Seistrup"""

    db = Geocoder()
    city = db["Abu Dhabi,United Arab Emirates"]
    assert city.name == "Abu Dhabi"

    city = db["Abu Dhabi,UAE"]
    assert city.name == "Abu Dhabi"


def test_Adelaide():
    """Test for fix made due to bug report from Klaus Alexander Seistrup"""

    db = Geocoder()
    _city = db["Adelaide"]


def test_CandianCities():
    db = Geocoder()

    city = db["Fredericton"]
    assert city.elevation == 8


def test_AllCities():
    db = Geocoder()
    locations = db.locations
    locations.sort()

    for city_name in locations:
        _city = db[city_name]
