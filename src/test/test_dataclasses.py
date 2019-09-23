import pytest

from astral import Observer, LocationInfo


def test_Observer_Default():
    obs = Observer()
    assert obs.latitude == 51.4733
    assert obs.longitude == -0.00088
    assert obs.elevation == 24.0


def test_Observer_FromFloat():
    obs = Observer(1, 1, 1)
    assert obs.latitude == 1.0
    assert obs.longitude == 1.0
    assert obs.elevation == 1.0


def test_Observer_FromString():
    obs = Observer("1", "2", "3")
    assert obs.latitude == 1.0
    assert obs.longitude == 2.0
    assert obs.elevation == 3.0


def test_Observer_BadLat():
    with pytest.raises(ValueError):
        Observer("o", 1, 1)


def test_Observer_BadLng():
    with pytest.raises(ValueError):
        Observer(1, "o", 1)


def test_Observer_BadElevaion():
    with pytest.raises(ValueError):
        Observer(1, 1, "o")


def test_LocationInfo_Default():
    li = LocationInfo()
    assert li.name == "Greenwich"
    assert li.region == "England"
    assert li.timezone == "Europe/London"
    assert li.latitude == 51.4733
    assert li.longitude == -0.00088
    assert li.elevation == 24.0


def test_Location_TimezoneGroup():
    li = LocationInfo()
    assert li.timezone_group == "Europe"
