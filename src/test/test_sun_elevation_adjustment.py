# -*- coding: utf-8 -*-

import pytest

from astral.sun import depression_at_elevation


def test_ElevationPositive():
    adjustment = depression_at_elevation(12000)
    assert pytest.approx(adjustment, 1.75887208410509)


def test_ElevationNegative():
    adjustment = depression_at_elevation(-1)
    assert pytest.approx(adjustment, 0)
