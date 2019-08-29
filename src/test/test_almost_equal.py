import datetime

from almost_equal import datetime_almost_equal


def test_datetime_almost_equal_Equal():
    d1 = datetime.datetime(2019, 1, 1)
    d2 = datetime.datetime(2019, 1, 1)

    assert datetime_almost_equal(d1, d2)


def test_datetime_almost_equal_NotEqual():
    d1 = datetime.datetime(2019, 1, 1)
    d2 = datetime.datetime(2019, 1, 1, 12, 2, 0)

    assert not datetime_almost_equal(d1, d2)


def test_datetime_almost_equal_EqualWithDelta():
    d1 = datetime.datetime(2019, 1, 1, 12, 0, 0)
    d2 = datetime.datetime(2019, 1, 1, 12, 2, 0)

    assert datetime_almost_equal(d1, d2, 121)
