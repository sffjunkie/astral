# -*- coding: utf-8 -*-
from astral.geocoder import lookup


def test_BuenosAries(test_database):
    b = lookup("Buenos Aires", test_database)
    assert b.timezone == "America/Buenos_Aires"
