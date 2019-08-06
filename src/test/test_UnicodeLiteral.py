# -*- coding: utf-8 -*-

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
