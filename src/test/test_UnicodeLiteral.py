# -*- coding: utf-8 -*-

# Import unicode_literals as that caused problems with the code
# See bug https://bugs.launchpad.net/astral/+bug/1588198 
from __future__ import unicode_literals
import os
import sys
sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest 
import astral

@pytest.mark.py2only
def test_Location_WithUnicodeLiteral():
    a = astral.Astral()
    _l = a['London']


@pytest.mark.py2only
def test_Latitude_WithUnicodeLiteral():
    l = astral.Location(('a place', 'a region', 1, 1))
    l.latitude = "24°28'N"


@pytest.mark.py2only
def test_Longitude_WithUnicodeLiteral():
    l = astral.Location(('a place', 'a region', 1, 1))
    l.longitude = "54°22'E"


@pytest.mark.py2only
def test_Depression_WithUnicodeLiteral():
    l = astral.Location(('a place', 'a region', 1, 1))
    l.solar_depression = 'civil'
    