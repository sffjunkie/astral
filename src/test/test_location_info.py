from astral import LocationInfo


def test_elevation():
    loc = LocationInfo("A place", "Somewhere", "Europe/London", 1, 2, 4)
    assert loc.elevation == 4


def test_elevation_string():
    loc = LocationInfo("A place", "Somewhere", "Europe/London", 1, 2, "3")
    assert loc.elevation == 3
