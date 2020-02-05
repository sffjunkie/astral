import pytest

from astral import Observer


class TestObserver:
    def test_default(self):
        obs = Observer()
        assert obs.latitude == 51.4733
        assert obs.longitude == -0.0008333
        assert obs.elevation == 0.0

    def test_from_float(self):
        obs = Observer(1, 1, 1)
        assert obs.latitude == 1.0
        assert obs.longitude == 1.0
        assert obs.elevation == 1.0

    def test_from_string(self):
        obs = Observer("1", "2", "3")
        assert obs.latitude == 1.0
        assert obs.longitude == 2.0
        assert obs.elevation == 3.0

    def test_from_dms(self):
        obs = Observer("24°N", "22°30'S", "3")
        assert obs.latitude == 24.0
        assert obs.longitude == -22.5
        assert obs.elevation == 3.0

    def test_bad_latitude(self):
        with pytest.raises(ValueError):
            Observer("o", 1, 1)

    def test_bad_longitude(self):
        with pytest.raises(ValueError):
            Observer(1, "o", 1)

    def test_bad_elevation(self):
        with pytest.raises(ValueError):
            Observer(1, 1, "o")

    def test_latitude_outside_limits(self):
        obs = Observer(90.1, 0, 0)
        assert obs.latitude == 90.0
        obs = Observer(-90.1, 0, 0)
        assert obs.latitude == -90.0

    def test_longitude_outside_limits(self):
        obs = Observer(0, 180.1, 0)
        assert obs.longitude == 180.0
        obs = Observer(0, -180.1, 0)
        assert obs.longitude == -180.0
