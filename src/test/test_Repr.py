# -*- coding: utf-8 -*-
from astral import LocationInfo
from astral.location import Location


class TestLocationRepr:
    def test_default(self):
        location = Location()
        assert (
            location.__repr__()
            == "Greenwich/England, tz=Europe/London, lat=51.47, lon=-0.00"
        )

    def test_full(self):
        location = Location(
            LocationInfo("London", "England", "Europe/London", 51.68, -0.05)
        )
        assert (
            location.__repr__()
            == "London/England, tz=Europe/London, lat=51.68, lon=-0.05"
        )

    def test_no_region(self):
        location = Location(
            LocationInfo(
                "London",
                None,
                "Europe/London",
                51.68,
                -0.05,
            )
        )
        assert location.__repr__() == ("London, tz=Europe/London, lat=51.68, lon=-0.05")
