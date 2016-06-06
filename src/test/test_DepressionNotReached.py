# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest 
import astral


def test_Dawn_NeverReachesDepression():
    with pytest.raises(astral.AstralError):
        a = astral.Astral()
        l = a['London']
        l.solar_depression = 18
        l.dawn(local=True)
