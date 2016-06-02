# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest 
import astral


def test_GhentDawn_NeverReachesDepression():
    with pytest.raises(astral.AstralError):
        a = astral.Astral(astral.GoogleGeocoder)
        l = a['Ghent,Belgium']
        l.solar_depression = 18
        l.dawn(local=True)
