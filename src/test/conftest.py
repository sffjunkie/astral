import datetime
import pytest
from astral import LocationInfo
from astral.geocoder import LocationDatabase, database
from astral.location import Location


@pytest.fixture
def astral_database() -> LocationDatabase:
    return database()


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
        "Riyadh", "Saudi Arabia", "Asia/Riyadh", 24.71355, 46.67530, 612
    )


@pytest.fixture
def riyadh(riyadh_info) -> Location:
    return Location(riyadh_info)


@pytest.fixture
def julian_day_test_data():
    return [
        (datetime.date(2012, 1, 1), 2455927.5),
        (datetime.date(2013, 1, 1), 2456293.5),
        (datetime.date(2013, 6, 1), 2456444.5),
        (datetime.date(1867, 2, 1), 2402998.5),
        (datetime.date(3200, 11, 14), 2890153.5),
    ]


@pytest.fixture
def julian_century_test_data():
    return [
        (2455927.5, 0.119986311),
        (2456293.5, 0.130006845),
        (2456444.5, 0.134140999),
        (2402998.5, -1.329130732),
        (2890153.5, 12.00844627),
    ]
