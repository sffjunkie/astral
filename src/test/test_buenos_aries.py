# -*- coding: utf-8 -*-
from astral.geocoder import lookup


def test_BuenosAries(astral_database):
    b = lookup("Buenos Aires", astral_database)
    assert b.timezone == "America/Buenos_Aires"
