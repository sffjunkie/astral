# Test data taken from http://www.timeanddate.com/sun/uk/london

import pytest
import pytz
import datetime
from astral import AstralError
from astral import calc
from astral.calc import SunDirection


def datetime_almost_equal(datetime1, datetime2, seconds=60):
    dd = datetime1 - datetime2
    sd = (dd.days * 24 * 60 * 60) + dd.seconds
    return abs(sd) <= seconds


def test_Astral_Sun(london):
    test_data = {
        datetime.date(2015, 12, 1): datetime.datetime(2015, 12, 1, 7, 4, 18),
        datetime.date(2015, 12, 2): datetime.datetime(2015, 12, 2, 7, 5, 34),
        datetime.date(2015, 12, 3): datetime.datetime(2015, 12, 3, 7, 6, 49),
        datetime.date(2015, 12, 12): datetime.datetime(2015, 12, 12, 7, 16, 37),
        datetime.date(2015, 12, 25): datetime.datetime(2015, 12, 25, 7, 25, 1),
    }

    for day, dawn in test_data.items():
        dawn = pytz.utc.localize(dawn)
        dawn_utc = calc.sun(london, day)["dawn"]
        assert datetime_almost_equal(dawn, dawn_utc)


def test_Astral_Dawn_Civil(london):
    test_data = {
        datetime.date(2015, 12, 1): datetime.datetime(2015, 12, 1, 7, 4, 18),
        datetime.date(2015, 12, 2): datetime.datetime(2015, 12, 2, 7, 5, 34),
        datetime.date(2015, 12, 3): datetime.datetime(2015, 12, 3, 7, 6, 49),
        datetime.date(2015, 12, 12): datetime.datetime(2015, 12, 12, 7, 16, 37),
        datetime.date(2015, 12, 25): datetime.datetime(2015, 12, 25, 7, 25, 1),
    }

    for day, dawn in test_data.items():
        dawn = pytz.utc.localize(dawn)
        dawn_utc = calc.dawn(london, day)
        assert datetime_almost_equal(dawn, dawn_utc)


def test_Astral_Dawn_Nautical(london):
    test_data = {
        datetime.date(2015, 12, 1): datetime.datetime(2015, 12, 1, 6, 22, 5),
        datetime.date(2015, 12, 2): datetime.datetime(2015, 12, 2, 6, 23, 17),
        datetime.date(2015, 12, 3): datetime.datetime(2015, 12, 3, 6, 24, 27),
        datetime.date(2015, 12, 12): datetime.datetime(2015, 12, 12, 6, 33, 40),
        datetime.date(2015, 12, 25): datetime.datetime(2015, 12, 25, 6, 41, 51),
    }

    for day, dawn in test_data.items():
        dawn = pytz.utc.localize(dawn)
        dawn_utc = calc.dawn(london, day, 12)
        assert datetime_almost_equal(dawn, dawn_utc)


def test_Astral_Sunrise(london):
    test_data = {
        datetime.date(2015, 1, 1): datetime.datetime(2015, 1, 1, 8, 6, 11),
        datetime.date(2015, 12, 1): datetime.datetime(2015, 12, 1, 7, 43, 17),
        datetime.date(2015, 12, 2): datetime.datetime(2015, 12, 2, 7, 44, 40),
        datetime.date(2015, 12, 3): datetime.datetime(2015, 12, 3, 7, 46, 2),
        datetime.date(2015, 12, 12): datetime.datetime(2015, 12, 12, 7, 56, 37),
        datetime.date(2015, 12, 25): datetime.datetime(2015, 12, 25, 8, 5, 18),
    }

    for day, sunrise in test_data.items():
        sunrise = pytz.utc.localize(sunrise)
        sunrise_utc = calc.sunrise(london, day)
        assert datetime_almost_equal(sunrise, sunrise_utc)


def test_Astral_Sunset(london):
    test_data = {
        datetime.date(2015, 1, 1): datetime.datetime(2015, 1, 1, 16, 1, 52),
        datetime.date(2015, 12, 1): datetime.datetime(2015, 12, 1, 15, 55, 13),
        datetime.date(2015, 12, 2): datetime.datetime(2015, 12, 2, 15, 54, 36),
        datetime.date(2015, 12, 3): datetime.datetime(2015, 12, 3, 15, 54, 2),
        datetime.date(2015, 12, 12): datetime.datetime(2015, 12, 12, 15, 51, 23),
        datetime.date(2015, 12, 25): datetime.datetime(2015, 12, 25, 15, 55, 35),
    }

    for day, sunset in test_data.items():
        sunset = pytz.utc.localize(sunset)
        sunset_utc = calc.sunset(london, day)
        assert datetime_almost_equal(sunset, sunset_utc)


def test_Astral_Dusk_Civil(london):
    test_data = {
        datetime.date(2015, 12, 1): datetime.datetime(2015, 12, 1, 16, 34),
        datetime.date(2015, 12, 2): datetime.datetime(2015, 12, 2, 16, 34),
        datetime.date(2015, 12, 3): datetime.datetime(2015, 12, 3, 16, 33),
        datetime.date(2015, 12, 12): datetime.datetime(2015, 12, 12, 16, 31),
        datetime.date(2015, 12, 25): datetime.datetime(2015, 12, 25, 16, 36),
    }

    for day, dusk in test_data.items():
        dusk = pytz.utc.localize(dusk)
        dusk_utc = calc.dusk(london, day)
        assert datetime_almost_equal(dusk, dusk_utc)


def test_Astral_Dusk_Nautical(london):
    test_data = {
        datetime.date(2015, 12, 1): datetime.datetime(2015, 12, 1, 17, 16),
        datetime.date(2015, 12, 2): datetime.datetime(2015, 12, 2, 17, 16),
        datetime.date(2015, 12, 3): datetime.datetime(2015, 12, 3, 17, 16),
        datetime.date(2015, 12, 12): datetime.datetime(2015, 12, 12, 17, 14),
        datetime.date(2015, 12, 25): datetime.datetime(2015, 12, 25, 17, 19),
    }

    for day, dusk in test_data.items():
        dusk = pytz.utc.localize(dusk)
        dusk_utc = calc.dusk(london, day, 12)
        assert datetime_almost_equal(dusk, dusk_utc)


def test_Astral_SolarNoon(london):
    test_data = {
        datetime.date(2015, 12, 1): datetime.datetime(2015, 12, 1, 11, 49),
        datetime.date(2015, 12, 2): datetime.datetime(2015, 12, 2, 11, 50),
        datetime.date(2015, 12, 3): datetime.datetime(2015, 12, 3, 11, 50),
        datetime.date(2015, 12, 12): datetime.datetime(2015, 12, 12, 11, 54),
        datetime.date(2015, 12, 25): datetime.datetime(2015, 12, 25, 12, 00),
    }

    for day, solar_noon in test_data.items():
        solar_noon = pytz.utc.localize(solar_noon)
        solar_noon_utc = calc.solar_noon(london, day)
        assert datetime_almost_equal(solar_noon, solar_noon_utc)


def test_Astral_SolarMidnight(london):
    test_data = {
        datetime.date(2016, 2, 18): datetime.datetime(2016, 2, 18, 0, 14),
        datetime.date(2016, 10, 26): datetime.datetime(2016, 10, 25, 23, 44),
    }

    for day, solar_midnight in test_data.items():
        solar_midnight = pytz.utc.localize(solar_midnight)
        solar_midnight_utc = calc.solar_midnight(london, day)
        assert datetime_almost_equal(solar_midnight, solar_midnight_utc)


# Test data from http://www.astroloka.com/rahukaal.aspx?City=Delhi
def test_Astral_Rahukaalam(new_delhi):
    test_data = {
        datetime.date(2015, 12, 1): (
            datetime.datetime(2015, 12, 1, 9, 17),
            datetime.datetime(2015, 12, 1, 10, 36, 16),
        ),
        datetime.date(2015, 12, 2): (
            datetime.datetime(2015, 12, 2, 6, 40),
            datetime.datetime(2015, 12, 2, 7, 58),
        ),
    }

    for day, (start, end) in test_data.items():
        start = pytz.utc.localize(start)
        end = pytz.utc.localize(end)

        info = calc.rahukaalam(new_delhi, day)
        start_utc = info[0]
        end_utc = info[1]
        assert datetime_almost_equal(start, start_utc)
        assert datetime_almost_equal(end, end_utc)


def test_Astral_SolarAltitude(london):
    test_data = {
        datetime.datetime(2015, 12, 14, 11, 0, 0): 14.41614,
        datetime.datetime(2015, 12, 14, 20, 1, 0): -37.5254,
    }

    for dt, angle1 in test_data.items():
        angle2 = calc.altitude(london, dt)
        assert pytest.approx(angle1, angle2)


def test_Astral_SolarAzimuth(london):
    test_data = {
        datetime.datetime(2015, 12, 14, 11, 0, 0, tzinfo=pytz.utc): 167,
        datetime.datetime(2015, 12, 14, 20, 1, 0): 279,
    }

    for dt, angle1 in test_data.items():
        angle2 = calc.azimuth(london, dt)
        assert pytest.approx(angle1, angle2)


def test_Astral_TimeAtAltitude_SunRising(london):
    d = datetime.date(2016, 1, 4)
    dt = calc.time_at_altitude(london, 6, d, SunDirection.RISING)
    cdt = datetime.datetime(2016, 1, 4, 9, 5, 0, tzinfo=pytz.utc)
    # Use error of 5 minutes as website has a rather coarse accuracy
    assert datetime_almost_equal(dt, cdt, 300)


def test_Astral_TimeAtAltitude_SunSetting(london):
    d = datetime.date(2016, 1, 4)
    dt = calc.time_at_altitude(london, 14, d, SunDirection.SETTING)
    cdt = datetime.datetime(2016, 1, 4, 13, 20, 0, tzinfo=pytz.utc)
    assert datetime_almost_equal(dt, cdt, 300)


def test_Astral_TimeAtAltitude_GreaterThan90(london):
    d = datetime.date(2016, 1, 4)
    dt = calc.time_at_altitude(london, 166, d, SunDirection.RISING)
    cdt = datetime.datetime(2016, 1, 4, 13, 20, 0, tzinfo=pytz.utc)
    assert datetime_almost_equal(dt, cdt, 300)


def test_Astral_TimeAtAltitude_GreaterThan180(london):
    d = datetime.date(2015, 12, 1)
    dt = calc.time_at_altitude(london, 186, d, SunDirection.RISING)
    cdt = datetime.datetime(2015, 12, 1, 16, 34, tzinfo=pytz.utc)
    assert datetime_almost_equal(dt, cdt, 300)


def test_Astral_TimeAtAltitude_SunRisingBelowHorizon(london):
    d = datetime.date(2016, 1, 4)
    dt = calc.time_at_altitude(london, -18, d, SunDirection.RISING)
    cdt = datetime.datetime(2016, 1, 4, 6, 0, 0, tzinfo=pytz.utc)
    assert datetime_almost_equal(dt, cdt, 300)


def test_Astral_TimeAtAltitude_BadElevation(london):
    d = datetime.date(2016, 1, 4)
    with pytest.raises(AstralError):
        calc.time_at_altitude(london, 20, d, SunDirection.RISING)


def test_Astral_Daylight(london):
    d = datetime.date(2016, 1, 6)
    start, end = calc.daylight(london, d)
    cstart = datetime.datetime(2016, 1, 6, 8, 5, 0, tzinfo=pytz.utc)
    cend = datetime.datetime(2016, 1, 6, 16, 7, 0, tzinfo=pytz.utc)
    assert datetime_almost_equal(start, cstart, 300)
    assert datetime_almost_equal(end, cend, 300)


def test_Astral_Nighttime(london):
    d = datetime.date(2016, 1, 6)
    start, end = calc.night(london, d)
    cstart = datetime.datetime(2016, 1, 6, 16, 46, 52, tzinfo=pytz.utc)
    cend = datetime.datetime(2016, 1, 7, 7, 25, 19, tzinfo=pytz.utc)
    assert datetime_almost_equal(start, cstart, 300)
    assert datetime_almost_equal(end, cend, 300)
