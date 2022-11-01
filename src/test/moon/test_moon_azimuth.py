import datetime

import pytest

from astral import Observer
from astral.location import Location
from astral.moon import azimuth


@pytest.mark.parametrize(
    "dt,value",
    [
        (datetime.datetime(2022, 10, 6, 1, 10, 0), 240.0),
        (datetime.datetime(2022, 10, 6, 16, 45, 0), 115.0),
        (datetime.datetime(2022, 10, 10, 6, 43, 0), 281.0),
        (datetime.datetime(2022, 10, 10, 3, 0, 0), 235.0),
    ],
)
def test_moon_azimuth(dt: datetime.datetime, value: float, london: Location):
    az = azimuth(london.observer, dt)
    assert pytest.approx(az, abs=1) == value  # type: ignore


def print_moon_azimuth():
    o = Observer(51.5, -0.13)
    for hour in range(24):
        d = datetime.datetime(2022, 10, 10, hour, 0, 0)
        print(hour, " 0", azimuth(o, d))
        d = datetime.datetime(2022, 10, 10, hour, 30, 0)
        print(hour, "30", azimuth(o, d))


if __name__ == "__main__":
    print_moon_azimuth()
