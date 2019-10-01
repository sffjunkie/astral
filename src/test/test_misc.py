from pytest import approx, raises
from datetime import timedelta
from astral import latlng_to_float
from astral.sun import minutes_to_timedelta


def test_MinutesToTime():
    assert minutes_to_timedelta(720) == timedelta(seconds=720 * 60)
    assert minutes_to_timedelta(722) == timedelta(seconds=722 * 60)
    assert minutes_to_timedelta(722.2) == timedelta(seconds=722.2 * 60)
    assert minutes_to_timedelta(722.5) == timedelta(seconds=722.5 * 60)


class TestDMS:
    def test_North(self):
        assert approx(latlng_to_float("24°28'N"), 24.466666)

    def test_whole_number_of_degrees(self):
        assert latlng_to_float("24°") == 24

    def test_East(self):
        assert approx(latlng_to_float("54°22'E"), 54.366666)

    def test_South(self):
        assert approx(latlng_to_float("37°58'S"), -37.966666)

    def test_West(self):
        assert approx(latlng_to_float("171°50'W"), 171.833333)

    def test_WestLowercase(self):
        assert approx(latlng_to_float("171°50'w"), 171.833333)

    def test_float(self):
        assert latlng_to_float("0.2") == 0.2

    def test_not_a_float(self):
        with raises(ValueError):
            latlng_to_float("x")
