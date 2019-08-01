# -*- coding: utf-8 -*-
from astral.geocoder import lookup


def test_BuenosAries():
    b = lookup("Buenos Aires")
    assert b.timezone == "America/Buenos_Aires"
