from datetime import timedelta

import freezegun
from pytest import approx, raises
from pytz import timezone

from astral import latlng_to_float, now, today
from astral.sun import minutes_to_timedelta


def test_MinutesToTimedelta():
    assert minutes_to_timedelta(720) == timedelta(seconds=720 * 60)
    assert minutes_to_timedelta(722) == timedelta(seconds=722 * 60)
    assert minutes_to_timedelta(722.2) == timedelta(seconds=722.2 * 60)
    assert minutes_to_timedelta(722.5) == timedelta(seconds=722.5 * 60)


class TestDMS:
    """Test degrees/minutes/seconds conversion functions"""

    def test_North(self):
        assert approx(latlng_to_float("24°28'N", 90), 24.466666)

    def test_whole_number_of_degrees(self):
        assert latlng_to_float("24°", 90) == 24

    def test_East(self):
        assert approx(latlng_to_float("54°22'E", 180), 54.366666)

    def test_South(self):
        assert approx(latlng_to_float("37°58'S", 90), -37.966666)

    def test_West(self):
        assert approx(latlng_to_float("171°50'W", 180), 171.833333)

    def test_WestLowercase(self):
        assert approx(latlng_to_float("171°50'w", 180), -171.833333)

    def test_float(self):
        assert latlng_to_float("0.2", 90) == 0.2

    def test_not_a_float(self):
        with raises(ValueError):
            latlng_to_float("x", 90)

    def test_latlng_outside_limit(self):
        with raises(ValueError):
            latlng_to_float("180°50'w", 180)


class TestToday:
    @freezegun.freeze_time("2020-01-01 14:00:00")
    def test_default_timezone(self):
        td = today()
        assert td.year == 2020
        assert td.month == 1
        assert td.day == 1

    @freezegun.freeze_time("2020-01-01 14:00:00")
    def test_australia(self):
        assert today(timezone("Australia/Melbourne")).day == 2

    @freezegun.freeze_time("2020-01-02 05:00:00")
    def test_adak(self):
        assert today(timezone("America/Adak")).day == 1


class TestNow:
    @freezegun.freeze_time("2020-01-01 14:10:20")
    def test_default_timezone(self):
        td = now()
        assert td.hour == 14
        assert td.minute == 10
        assert td.second == 20
