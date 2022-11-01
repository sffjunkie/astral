# -*- coding: utf-8 -*-

import datetime

import pytest

from astral import LocationInfo
from astral.location import Location


def test_Dawn_NeverReachesDepression():
    d = datetime.date(2016, 5, 29)
    with pytest.raises(ValueError):
        loc = Location(
            LocationInfo(
                "Ghent",
                "Belgium",
                "Europe/Brussels",
                "51°3'N",
                "3°44'W",
            )  # type: ignore
        )
        loc.solar_depression = 18
        loc.dawn(date=d, local=True)
