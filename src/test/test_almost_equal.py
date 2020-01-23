import datetime

from almost_equal import datetime_almost_equal


class TestDateTimeAlmostEqual:
    """Test the datetime comparison function"""

    def test_equal(self):
        d1 = datetime.datetime(2019, 1, 1)
        d2 = datetime.datetime(2019, 1, 1)

        assert datetime_almost_equal(d1, d2)

    def test_not_equal(self):
        d1 = datetime.datetime(2019, 1, 1)
        d2 = datetime.datetime(2019, 1, 1, 12, 2, 0)

        assert not datetime_almost_equal(d1, d2)

    def test_equal_with_delta(self):
        d1 = datetime.datetime(2019, 1, 1, 12, 0, 0)
        d2 = datetime.datetime(2019, 1, 1, 12, 2, 0)

        assert datetime_almost_equal(d1, d2, 121)
