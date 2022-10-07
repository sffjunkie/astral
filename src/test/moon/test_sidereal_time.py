import datetime

from astral import hours_to_time
from astral.sidereal import gmst, lmst


def test_gmst():
    dt = datetime.datetime(1987, 4, 10, 0, 0, 0)
    mean_sidereal_time = gmst(dt)

    t = hours_to_time(mean_sidereal_time / 15)
    assert t.hour == 13
    assert t.minute == 10
    assert t.second == 46
    assert t.microsecond == 366821


def test_gmst_with_time():
    dt = datetime.datetime(1987, 4, 10, 19, 21, 0)
    mean_sidereal_time = gmst(dt)
    t = hours_to_time(mean_sidereal_time / 15)
    assert t.hour == 8
    assert t.minute == 34
    assert t.second == 57
    assert t.microsecond == 89578


def test_local_mean_sidereal_time():
    dt = datetime.datetime(1987, 4, 10, 0, 0, 0)
    mean_sidereal_time = lmst(dt, -0.13)
    assert mean_sidereal_time == 197.693195090862 - 0.13
