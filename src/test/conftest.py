import pytest
from astral import LocationInfo, Observer
from astral.location import Location


@pytest.fixture
def london_info() -> LocationInfo:
    return LocationInfo("London", "England", "Europe/London", 51.50853, -0.12574, 24)


@pytest.fixture
def london(london_info) -> Location:
    return Location(london_info)


@pytest.fixture
def new_delhi_info() -> LocationInfo:
    return LocationInfo("New Delhi", "India", "Asia/Kolkata", 28.61, 77.22, 233)


@pytest.fixture
def new_delhi(new_delhi_info) -> Location:
    return Location(new_delhi_info)


@pytest.fixture
def riyadh_info() -> LocationInfo:
    return LocationInfo(
        "riyadh", "Saudi Arabia", "Asia/Riyadh", 24.71355, 46.67530, 612
    )


@pytest.fixture
def riyadh(riyadh_info) -> Location:
    return Location(riyadh_info)
