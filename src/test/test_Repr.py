# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from astral import Astral, Location

def test_LocationRepr():
    l = Location(('London', 'England', 51.68, -0.05, 'Europe/London', 3))
    assert l.__repr__() == 'London/England, tz=Europe/London, lat=51.68, lon=-0.05'
