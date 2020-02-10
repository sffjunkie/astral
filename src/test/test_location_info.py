import pytest
from astral import LocationInfo


class TestLocationInfo:
    def test_Default(self):
        loc = LocationInfo()
        assert loc.name == "Greenwich"
        assert loc.region == "England"
        assert loc.timezone == "Europe/London"
        assert loc.latitude == pytest.approx(51.4733, abs=0.001)
        assert loc.longitude == pytest.approx(-0.0008333, abs=0.000001)

    def test_bad_latitude(self):
        with pytest.raises(ValueError):
            LocationInfo("A place", "Somewhere", "Europe/London", "i", 2)

    def test_bad_longitude(self):
        with pytest.raises(ValueError):
            LocationInfo("A place", "Somewhere", "Europe/London", 2, "i")

    def test_timezone_group(self):
        li = LocationInfo()
        assert li.timezone_group == "Europe"
