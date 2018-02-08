# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import pytest
import astral
import datetime


def test_Dawn_NeverReachesDepression():
    d = datetime.date(2016, 5, 29)
    with pytest.raises(astral.AstralError):
        l = astral.Location(("Ghent", "Belgium", "51°3'N", "3°44'W", "Europe/Brussels"))
        l.solar_depression = 18
        l.dawn(date=d, local=True)
