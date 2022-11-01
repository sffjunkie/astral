import datetime

import astral
import astral.sun


def test_value_error_bug():
    loc = astral.LocationInfo(
        name="Barwani",
        region="India",
        timezone="Asia/Kolkata",
        latitude=23.518507,
        longitude=74.952246,
    )
    ob = loc.observer
    sun = astral.sun.sun(ob, date=datetime.date(2022, 7, 20))
    dawn = sun["dawn"]


if __name__ == "__main__":
    test_value_error_bug()
