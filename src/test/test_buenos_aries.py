# -*- coding: utf-8 -*-
from astral.location import LocationInfo
from astral.geocoder import lookup, LocationDatabase


def test_BuenosAries(test_database: LocationDatabase):
    b = lookup("Buenos Aires", test_database)
    assert isinstance(b, LocationInfo)
    assert b.timezone == "America/Buenos_Aires"
