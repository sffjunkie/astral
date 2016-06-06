# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from astral import Astral, Location

def test_BuenosAries():
    a = Astral()
    b = a['Buenos Aires']
    assert b.timezone == 'America/Buenos_Aires'
    