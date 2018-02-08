# -*- coding: utf-8 -*-
from astral import Astral, Location

def test_BuenosAries():
    a = Astral()
    b = a['Buenos Aires']
    assert b.timezone == 'America/Buenos_Aires'
