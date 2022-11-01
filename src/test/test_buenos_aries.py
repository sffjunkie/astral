# -*- coding: utf-8 -*-
from astral.geocoder import LocationDatabase, lookup
from astral.location import LocationInfo


def test_BuenosAries(test_database: LocationDatabase):
    b = lookup("Buenos Aires", test_database)
    assert isinstance(b, LocationInfo)
    assert b.timezone == "America/Buenos_Aires"
