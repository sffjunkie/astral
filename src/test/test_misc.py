from datetime import timedelta

import freezegun
from pytest import approx, raises
from pytz import timezone

from astral import dms_to_float, now, today
from astral.sun import minutes_to_timedelta


def test_MinutesToTimedelta():
    assert minutes_to_timedelta(720) == timedelta(seconds=720 * 60)
    assert minutes_to_timedelta(722) == timedelta(seconds=722 * 60)
    assert minutes_to_timedelta(722.2) == timedelta(seconds=722.2 * 60)
    assert minutes_to_timedelta(722.5) == timedelta(seconds=722.5 * 60)


class TestDMS:
    """Test degrees/minutes/seconds conversion functions"""

    def test_north(self):
        assert dms_to_float("24°28'N", 90) == approx(24.466666)

    def test_whole_number_of_degrees(self):
        assert dms_to_float("24°", 90.0) == 24.0

    def test_east(self):
        assert dms_to_float("54°22'E", 180.0) == approx(54.366666, abs=0.00001)

    def test_south(self):
        assert dms_to_float("37°58'S", 90.0) == approx(-37.966666, abs=0.00001)

    def test_west(self):
        assert dms_to_float("171°50'W", 180.0) == approx(-171.8333333, abs=0.00001)

    def test_west_lowercase(self):
        assert dms_to_float("171°50'w", 180.0) == approx(-171.8333333, abs=0.00001)

    def test_float(self):
        assert dms_to_float("0.2", 90.0) == 0.2

    def test_not_a_float(self):
        with raises(ValueError):
            dms_to_float("x", 90.0)

    def test_latlng_outside_limit(self):
        assert dms_to_float("180°50'w", 180.0) == -180


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

    @freezegun.freeze_time("2020-01-01 14:20:00")
    def test_australia(self):
        td = now(timezone("Australia/Melbourne"))
        assert td.hour == 1
        assert td.minute == 20
