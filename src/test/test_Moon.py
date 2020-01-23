# -*- coding: utf-8 -*-
import datetime

import pytest

from astral import moon


class TestMoon:
    """Moon phase"""

    @pytest.mark.parametrize(
        "date_,phase",
        [
            (datetime.date(2015, 12, 1), 19),
            (datetime.date(2015, 12, 2), 20),
            (datetime.date(2015, 12, 3), 21),
            (datetime.date(2014, 12, 1), 9),
            (datetime.date(2014, 12, 2), 10),
            (datetime.date(2014, 1, 1), 0),
        ],
    )
    def test_phase_number(self, date_, phase):
        """Test moon phase with default return type"""
        assert moon.phase(date_) == phase

    def test_phase_number_as_float(self):
        """Test moon phase with float return type"""
        d = datetime.date(2011, 1, 1)
        p = moon.phase(d, float)
        assert isinstance(p, float)
        assert p == pytest.approx(25.3, abs=0.1)

    def test_phase_number_as_int(self):
        """Test moon phase with int return type"""
        d = datetime.date(2011, 1, 1)
        p = moon.phase(d, int)
        assert isinstance(p, int)
        assert p == 25

    def test_bad_result_type(self):
        """Test moon phase with bad return type"""
        d = datetime.date(2011, 1, 1)
        assert moon.phase(d, str) == 25
