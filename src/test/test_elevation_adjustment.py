# -*- coding: utf-8 -*-
import pytest

from astral.sun.calc import adjustment_for_elevation


def test_ElevationPositive():
    adjustment = adjustment_for_elevation(12000)
    assert pytest.approx(adjustment, 1.75887208410509)


def test_ElevationNegative():
    adjustment = adjustment_for_elevation(-1)
    assert pytest.approx(adjustment, 0)
