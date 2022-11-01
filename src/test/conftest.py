import pytest

from astral import LocationInfo
from astral.geocoder import LocationDatabase, database
from astral.location import Location


@pytest.fixture
def test_database() -> LocationDatabase:
    return database()


@pytest.fixture
def london_info() -> LocationInfo:
    # return LocationInfo("London", "England", "Europe/London", 51.50853, -0.12574)
    return LocationInfo("London", "England", "Europe/London", 51.5, -0.1333333)


@pytest.fixture
def london(london_info: LocationInfo) -> Location:
    return Location(london_info)


@pytest.fixture
def new_delhi_info() -> LocationInfo:
    return LocationInfo("New Delhi", "India", "Asia/Kolkata", 28.61, 77.22)


@pytest.fixture
def new_delhi(new_delhi_info: LocationInfo) -> Location:
    return Location(new_delhi_info)


@pytest.fixture
def riyadh_info() -> LocationInfo:
    return LocationInfo("Riyadh", "Saudi Arabia", "Asia/Riyadh", 24.71355, 46.67530)


@pytest.fixture
def riyadh(riyadh_info: LocationInfo) -> Location:
    return Location(riyadh_info)


@pytest.fixture
def wellington_info() -> LocationInfo:
    return LocationInfo(
        "Wellington", "New Zealand", "Pacific/Auckland", -41.33, 174.766666
    )


@pytest.fixture
def wellington(wellington_info: LocationInfo) -> Location:
    return Location(wellington_info)


@pytest.fixture
def tromso_info() -> LocationInfo:
    return LocationInfo("Tromso", "Norway", "CET", 69.6, 18.95)


@pytest.fixture
def tromso(tromso_info: LocationInfo) -> Location:
    return Location(tromso_info)
