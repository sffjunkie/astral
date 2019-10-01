import pytest
from astral import LocationInfo


class TestLocationInfo:
    def test_Default(self):
        loc = LocationInfo()
        assert loc.name == "Greenwich"
        assert loc.region == "England"
        assert loc.timezone == "Europe/London"
        assert loc.latitude == 51.4733
        assert loc.longitude == -0.00088
        assert loc.elevation == 24.0

    def test_elevation(self):
        loc = LocationInfo("A place", "Somewhere", "Europe/London", 1, 2, 4)
        assert loc.elevation == 4

    def test_elevation_from_string(self):
        loc = LocationInfo("A place", "Somewhere", "Europe/London", 1, 2, "3")
        assert loc.elevation == 3

    def test_bad_latitude(self):
        with pytest.raises(ValueError):
            LocationInfo("A place", "Somewhere", "Europe/London", "i", 2, 1)

    def test_bad_longitude(self):
        with pytest.raises(ValueError):
            LocationInfo("A place", "Somewhere", "Europe/London", 2, "i", 1)

    def test_bad_elevation(self):
        with pytest.raises(ValueError):
            LocationInfo("A place", "Somewhere", "Europe/London", 1, 2, "i")

    def test_timezone_group(self):
        li = LocationInfo()
        assert li.timezone_group == "Europe"
