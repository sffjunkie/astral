# -*- coding: utf-8 -*-
import pytest

from astral import Astral

import datetime

def test_Astral_Moon_PhaseNumber():
    dates = {
        datetime.date(2015, 12, 1): 19,
        datetime.date(2015, 12, 2): 20,
        datetime.date(2015, 12, 3): 21,

        datetime.date(2014, 12, 1): 9,
        datetime.date(2014, 12, 2): 10,
        datetime.date(2014, 1, 1): 0,
    }

    a = Astral()

    for date_, moon in dates.items():
        assert a.moon_phase(date_) == moon


def test_Location_Moon_PhaseNumber():
    a = Astral()
    d = datetime.date(2011, 1, 1)

    l = a['London']
    assert l.moon_phase(d) == 25


def test_Location_Moon_PhaseNumberAsFloat():
    a = Astral()
    d = datetime.date(2011, 1, 1)

    l = a['London']
    assert l.moon_phase(d, float) == pytest.approx(25.3, abs=0.1)


def test_Location_Moon_Phase_BadRType():
    a = Astral()
    d = datetime.date(2011, 1, 1)

    l = a['London']
    assert l.moon_phase(d, str) == 25
