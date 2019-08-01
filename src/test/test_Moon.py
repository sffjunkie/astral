# -*- coding: utf-8 -*-
import datetime

import pytest

from astral import moon


def test_Astral_Moon_PhaseNumber():
    test_data = {
        datetime.date(2015, 12, 1): 19,
        datetime.date(2015, 12, 2): 20,
        datetime.date(2015, 12, 3): 21,
        datetime.date(2014, 12, 1): 9,
        datetime.date(2014, 12, 2): 10,
        datetime.date(2014, 1, 1): 0,
    }

    for date_, moon_phase in test_data.items():
        assert moon.phase(date_) == moon_phase


def test_Moon_PhaseNumberAsFloat():
    d = datetime.date(2011, 1, 1)
    p = moon.phase(d, float)
    assert isinstance(p, float)
    assert p == pytest.approx(25.3, abs=0.1)


def test_Moon_Phase_BadRType():
    d = datetime.date(2011, 1, 1)
    assert moon.phase(d, str) == 25
