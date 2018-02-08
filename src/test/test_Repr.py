# -*- coding: utf-8 -*-
from astral import Astral, Location

def test_LocationReprDefault():
    l = Location()
    assert l.__repr__() == 'Greenwich/England, tz=Europe/London, lat=51.17, lon=0.00'


def test_LocationReprFull():
    l = Location(('London', 'England', 51.68, -0.05, 'Europe/London', 3))
    assert l.__repr__() == 'London/England, tz=Europe/London, lat=51.68, lon=-0.05'


def test_LocationReprNoRegion():
    l = Location(('London', None, 51.68, -0.05, 'Europe/London', 3))
    assert l.__repr__() == 'London, tz=Europe/London, lat=51.68, lon=-0.05'
