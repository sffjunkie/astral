# -*- coding: utf-8 -*-
import pytest

import pytz
import datetime
import math
from astral import Astral

def float_almost_equal(value1, value2, diff=0.5):
    return abs(value1 - value2) <= diff


def test_ElevationPositive():
    dd = Astral()
    adjustment = dd._depression_adjustment(12000)
    assert float_almost_equal(adjustment, 1.75887208410509)


def test_ElevationNegative():
    dd = Astral()
    adjustment = dd._depression_adjustment(-1)
    assert float_almost_equal(adjustment, 0)
