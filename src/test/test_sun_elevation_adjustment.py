# -*- coding: utf-8 -*-
import pytest  # type: ignore

from astral.sun import adjust_to_horizon, adjust_to_obscuring_feature


class TestElevationAdjustment:
    def test_Float_Positive(self):
        adjustment = adjust_to_horizon(12000)
        assert adjustment == pytest.approx(3.517744168209966)

    def test_Float_Negative(self):
        adjustment = adjust_to_horizon(-1)
        assert adjustment == pytest.approx(0)

    def test_Tuple_0(self):
        adjustment = adjust_to_obscuring_feature((0.0, 100.0))
        assert adjustment == 0.0

    def test_Tuple_45deg(self):
        adjustment = adjust_to_obscuring_feature((10.0, 10.0))
        assert adjustment == pytest.approx(45.0)

    def test_Tuple_30deg(self):
        adjustment = adjust_to_obscuring_feature((3.0, 4.0))
        assert adjustment == pytest.approx(53.130102354156)

    def test_Tuple_neg45deg(self):
        adjustment = adjust_to_obscuring_feature((-10.0, 10.0))
        assert adjustment == pytest.approx(-45.0)
