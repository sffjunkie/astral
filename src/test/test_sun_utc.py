# Test data taken from http://www.timeanddate.com/sun/uk/london

from almost_equal import datetime_almost_equal
import pytest
import pytz
import datetime
import freezegun
from astral import sun
from astral.sun import SunDirection


@pytest.mark.parametrize(
    "day,dawn",
    [
        (datetime.date(2015, 12, 1), datetime.datetime(2015, 12, 1, 7, 3, 17)),
        (datetime.date(2015, 12, 2), datetime.datetime(2015, 12, 2, 7, 4, 34)),
        (datetime.date(2015, 12, 3), datetime.datetime(2015, 12, 3, 7, 5, 48)),
        (datetime.date(2015, 12, 12), datetime.datetime(2015, 12, 12, 7, 15, 36)),
        (datetime.date(2015, 12, 25), datetime.datetime(2015, 12, 25, 7, 24, 0)),
    ],
)
def test_Sun(day, dawn, london):
    dawn = pytz.utc.localize(dawn)
    dawn_utc = sun.sun(london, day)["dawn"]
    assert datetime_almost_equal(dawn, dawn_utc)


@freezegun.freeze_time("2015-12-01")
def test_Sun_NoDate(london):
    ans = pytz.utc.localize(datetime.datetime(2015, 12, 1, 7, 3, 17))
    assert datetime_almost_equal(sun.sun(london)["dawn"], ans)


@pytest.mark.parametrize(
    "day,dawn",
    [
        (datetime.date(2015, 12, 1), datetime.datetime(2015, 12, 1, 7, 3, 17)),
        (datetime.date(2015, 12, 2), datetime.datetime(2015, 12, 2, 7, 4, 34)),
        (datetime.date(2015, 12, 3), datetime.datetime(2015, 12, 3, 7, 5, 48)),
        (datetime.date(2015, 12, 12), datetime.datetime(2015, 12, 12, 7, 15, 36)),
        (datetime.date(2015, 12, 25), datetime.datetime(2015, 12, 25, 7, 24, 0)),
    ],
)
def test_Dawn_Civil(day, dawn, london):
    dawn = pytz.utc.localize(dawn)
    dawn_utc = sun.dawn(london, day, 6)
    assert datetime_almost_equal(dawn, dawn_utc)


@freezegun.freeze_time("2015-12-01")
def test_Dawn_NoDate(london):
    ans = pytz.utc.localize(datetime.datetime(2015, 12, 1, 7, 3, 17))
    assert datetime_almost_equal(sun.dawn(london), ans)


@pytest.mark.parametrize(
    "day,dawn",
    [
        (datetime.date(2015, 12, 1), datetime.datetime(2015, 12, 1, 6, 21, 17)),
        (datetime.date(2015, 12, 2), datetime.datetime(2015, 12, 2, 6, 22, 29)),
        (datetime.date(2015, 12, 3), datetime.datetime(2015, 12, 3, 6, 23, 39)),
        (datetime.date(2015, 12, 12), datetime.datetime(2015, 12, 12, 6, 32, 52)),
        (datetime.date(2015, 12, 25), datetime.datetime(2015, 12, 25, 6, 41, 5)),
    ],
)
def test_Dawn_Nautical(day, dawn, london):
    dawn = pytz.utc.localize(dawn)
    dawn_utc = sun.dawn(london, day, 12)
    assert datetime_almost_equal(dawn, dawn_utc)


@pytest.mark.parametrize(
    "day,dawn",
    [
        (datetime.date(2015, 12, 1), datetime.datetime(2015, 12, 1, 5, 41, 9)),
        (datetime.date(2015, 12, 2), datetime.datetime(2015, 12, 2, 5, 42, 18)),
        (datetime.date(2015, 12, 3), datetime.datetime(2015, 12, 3, 5, 43, 25)),
        (datetime.date(2015, 12, 12), datetime.datetime(2015, 12, 12, 5, 52, 17)),
        (datetime.date(2015, 12, 25), datetime.datetime(2015, 12, 25, 6, 0, 22)),
    ],
)
def test_Dawn_Astronomical(day, dawn, london):
    dawn = pytz.utc.localize(dawn)
    dawn_utc = sun.dawn(london, day, 18)
    assert datetime_almost_equal(dawn, dawn_utc)


@pytest.mark.parametrize(
    "day,sunrise",
    [
        (datetime.date(2015, 1, 1), datetime.datetime(2015, 1, 1, 8, 5, 54)),
        (datetime.date(2015, 12, 1), datetime.datetime(2015, 12, 1, 7, 43, 0)),
        (datetime.date(2015, 12, 2), datetime.datetime(2015, 12, 2, 7, 44, 24)),
        (datetime.date(2015, 12, 3), datetime.datetime(2015, 12, 3, 7, 45, 45)),
        (datetime.date(2015, 12, 12), datetime.datetime(2015, 12, 12, 7, 56, 20)),
        (datetime.date(2015, 12, 25), datetime.datetime(2015, 12, 25, 8, 5, 1)),
    ],
)
def test_Sunrise(day, sunrise, london):
    sunrise = pytz.utc.localize(sunrise)
    sunrise_utc = sun.sunrise(london, day)
    assert datetime_almost_equal(sunrise, sunrise_utc)


@freezegun.freeze_time("2015-12-01")
def test_Sunrise_NoDate(london):
    ans = pytz.utc.localize(datetime.datetime(2015, 12, 1, 7, 43, 0))
    assert datetime_almost_equal(sun.sunrise(london), ans)


@pytest.mark.parametrize(
    "day,sunset",
    [
        (datetime.date(2015, 1, 1), datetime.datetime(2015, 1, 1, 16, 2, 9)),
        (datetime.date(2015, 12, 1), datetime.datetime(2015, 12, 1, 15, 55, 29)),
        (datetime.date(2015, 12, 2), datetime.datetime(2015, 12, 2, 15, 54, 52)),
        (datetime.date(2015, 12, 3), datetime.datetime(2015, 12, 3, 15, 54, 18)),
        (datetime.date(2015, 12, 12), datetime.datetime(2015, 12, 12, 15, 51, 39)),
        (datetime.date(2015, 12, 25), datetime.datetime(2015, 12, 25, 15, 55, 52)),
    ],
)
def test_Sunset(day, sunset, london):
    sunset = pytz.utc.localize(sunset)
    sunset_utc = sun.sunset(london, day)
    assert datetime_almost_equal(sunset, sunset_utc)


@freezegun.freeze_time("2015-12-01")
def test_Sunset_NoDate(london):
    ans = pytz.utc.localize(datetime.datetime(2015, 12, 1, 15, 55, 29))
    assert datetime_almost_equal(sun.sunset(london), ans)


@pytest.mark.parametrize(
    "day,dusk",
    [
        (datetime.date(2015, 12, 1), datetime.datetime(2015, 12, 1, 16, 35, 11)),
        (datetime.date(2015, 12, 2), datetime.datetime(2015, 12, 2, 16, 34, 41)),
        (datetime.date(2015, 12, 3), datetime.datetime(2015, 12, 3, 16, 34, 14)),
        (datetime.date(2015, 12, 12), datetime.datetime(2015, 12, 12, 16, 32, 23)),
        (datetime.date(2015, 12, 25), datetime.datetime(2015, 12, 25, 16, 36, 53)),
    ],
)
def test_Dusk_Civil(day, dusk, london):
    dusk = pytz.utc.localize(dusk)
    dusk_utc = sun.dusk(london, day)
    assert datetime_almost_equal(dusk, dusk_utc)


@freezegun.freeze_time("2015-12-01")
def test_Dusk_NoDate(london):
    ans = pytz.utc.localize(datetime.datetime(2015, 12, 1, 16, 35, 11))
    assert datetime_almost_equal(sun.dusk(london), ans)


@pytest.mark.parametrize(
    "day,dusk",
    [
        (datetime.date(2015, 12, 1), datetime.datetime(2015, 12, 1, 17, 17, 10)),
        (datetime.date(2015, 12, 2), datetime.datetime(2015, 12, 2, 17, 16, 45)),
        (datetime.date(2015, 12, 3), datetime.datetime(2015, 12, 3, 17, 16, 22)),
        (datetime.date(2015, 12, 12), datetime.datetime(2015, 12, 12, 17, 15, 6)),
        (datetime.date(2015, 12, 25), datetime.datetime(2015, 12, 25, 17, 19, 49)),
    ],
)
def test_Dusk_Nautical(day, dusk, london):
    dusk = pytz.utc.localize(dusk)
    dusk_utc = sun.dusk(london, day, 12)
    assert datetime_almost_equal(dusk, dusk_utc)


@pytest.mark.parametrize(
    "day,noon",
    [
        (datetime.date(2015, 12, 1), datetime.datetime(2015, 12, 1, 11, 49, 14)),
        (datetime.date(2015, 12, 2), datetime.datetime(2015, 12, 2, 11, 49, 36)),
        (datetime.date(2015, 12, 3), datetime.datetime(2015, 12, 3, 11, 49, 59)),
        (datetime.date(2015, 12, 12), datetime.datetime(2015, 12, 12, 11, 53, 51)),
        (datetime.date(2015, 12, 25), datetime.datetime(2015, 12, 25, 12, 0, 10)),
    ],
)
def test_SolarNoon(day, noon, london):
    noon = pytz.utc.localize(noon)
    noon_utc = sun.noon(london, day)
    assert datetime_almost_equal(noon, noon_utc)


@freezegun.freeze_time("2015-12-01")
def test_SolarNoon_NoDate(london):
    ans = pytz.utc.localize(datetime.datetime(2015, 12, 1, 11, 49, 14))
    assert datetime_almost_equal(sun.noon(london), ans)


@pytest.mark.parametrize(
    "day,midnight",
    [
        (datetime.date(2016, 2, 18), datetime.datetime(2016, 2, 18, 0, 14, 28)),
        (datetime.date(2016, 10, 26), datetime.datetime(2016, 10, 25, 23, 44, 24)),
    ],
)
def test_SolarMidnight(day, midnight, london):
    solar_midnight = pytz.utc.localize(midnight)
    solar_midnight_utc = sun.midnight(london, day)
    assert datetime_almost_equal(solar_midnight, solar_midnight_utc)


@freezegun.freeze_time("2016-2-18")
def test_SolarMidnight_NoDate(london):
    ans = pytz.utc.localize(datetime.datetime(2016, 2, 18, 0, 14, 28))
    assert datetime_almost_equal(sun.midnight(london), ans)


@pytest.mark.parametrize(
    "day,twilight",
    [
        (
            datetime.date(2019, 8, 29),
            (
                datetime.datetime(2019, 8, 29, 4, 31, 21),
                datetime.datetime(2019, 8, 29, 5, 7, 27),
            ),
        ),
    ],
)
def test_Twilight_SunRising(day, twilight, london):
    start, end = twilight
    start = pytz.utc.localize(start)
    end = pytz.utc.localize(end)

    info = sun.twilight(london, day)
    start_utc = info[0]
    end_utc = info[1]
    assert datetime_almost_equal(start, start_utc)
    assert datetime_almost_equal(end, end_utc)


@pytest.mark.parametrize(
    "day,twilight",
    [
        (
            datetime.date(2019, 8, 29),
            (
                datetime.datetime(2019, 8, 29, 18, 54, 32),
                datetime.datetime(2019, 8, 29, 19, 30, 25),
            ),
        ),
    ],
)
def test_Twilight_SunSetting(day, twilight, london):
    start = pytz.utc.localize(twilight[0])
    end = pytz.utc.localize(twilight[1])

    info = sun.twilight(london, day, direction=SunDirection.SETTING)
    start_utc = info[0]
    end_utc = info[1]
    assert datetime_almost_equal(start, start_utc)
    assert datetime_almost_equal(end, end_utc)


@freezegun.freeze_time("2019-8-29")
def test_Twilight_NoDate(london):
    start = pytz.utc.localize(datetime.datetime(2019, 8, 29, 18, 54, 32))
    end = pytz.utc.localize(datetime.datetime(2019, 8, 29, 19, 30, 25))
    ans = sun.twilight(london, direction=SunDirection.SETTING)
    assert datetime_almost_equal(ans[0], start)
    assert datetime_almost_equal(ans[1], end)


# Test data from http://www.astroloka.com/rahukaal.aspx?City=Delhi
@pytest.mark.parametrize(
    "day,rahu",
    [
        (
            datetime.date(2015, 12, 1),
            (
                datetime.datetime(2015, 12, 1, 9, 17, 21),
                datetime.datetime(2015, 12, 1, 10, 36, 6),
            ),
        ),
        (
            datetime.date(2015, 12, 2),
            (
                datetime.datetime(2015, 12, 2, 6, 40, 14),
                datetime.datetime(2015, 12, 2, 7, 58, 53),
            ),
        ),
    ],
)
def test_Rahukaalam(day, rahu, new_delhi):
    start = pytz.utc.localize(rahu[0])
    end = pytz.utc.localize(rahu[1])

    info = sun.rahukaalam(new_delhi, day)
    start_utc = info[0]
    end_utc = info[1]
    assert datetime_almost_equal(start, start_utc)
    assert datetime_almost_equal(end, end_utc)


@freezegun.freeze_time("2015-12-01")
def test_Rahukaalam_NoDate(new_delhi):
    start = pytz.utc.localize(datetime.datetime(2015, 12, 1, 9, 17, 21))
    end = pytz.utc.localize(datetime.datetime(2015, 12, 1, 10, 36, 6))
    ans = sun.rahukaalam(new_delhi)
    assert datetime_almost_equal(ans[0], start)
    assert datetime_almost_equal(ans[1], end)


@pytest.mark.parametrize(
    "dt,altitude",
    [
        (datetime.datetime(2015, 12, 14, 11, 0, 0), 14.41614),
        (datetime.datetime(2015, 12, 14, 20, 1, 0), -37.5254),
    ],
)
def test_SolarAltitude(dt, altitude, london):
    angle = sun.elevation(london, dt)
    assert pytest.approx(altitude, angle)


@freezegun.freeze_time("2015-12-14 11:00:00", tz_offset=0)
def test_SolarAltitude_NoDate(london):
    assert pytest.approx(sun.elevation(london), 14.41614)


@pytest.mark.parametrize(
    "dt,azimuth",
    [
        (datetime.datetime(2015, 12, 14, 11, 0, 0, tzinfo=pytz.utc), 167),
        (datetime.datetime(2015, 12, 14, 20, 1, 0), 279),
    ],)
def test_SolarAzimuth(dt, azimuth, london):
    angle2 = sun.azimuth(london, dt)
    assert pytest.approx(azimuth, angle2)


@freezegun.freeze_time("2015-12-14 11:00:00", tz_offset=0)
def test_SolarAzimuth_NoDate(london):
    assert pytest.approx(sun.azimuth(london), 167)


def test_SolarZenith(london):
    test_data = {
        datetime.datetime(2019, 8, 29, 14, 34, 0, tzinfo=london.tzinfo): 46,
    }

    for dt, angle1 in test_data.items():
        angle2 = sun.zenith(london, dt)
        assert pytest.approx(angle1, angle2)


@freezegun.freeze_time("2019-08-29 14:34:00", tz_offset=1)
def test_SolarZenith_NoDate(london):
    assert pytest.approx(sun.zenith(london), 46)


def test_TimeAtAltitude_SunRising(london):
    d = datetime.date(2016, 1, 4)
    dt = sun.time_at_elevation(london, 6, d, SunDirection.RISING)
    cdt = datetime.datetime(2016, 1, 4, 9, 5, 0, tzinfo=pytz.utc)
    # Use error of 5 minutes as website has a rather coarse accuracy
    assert datetime_almost_equal(dt, cdt, 300)


@freezegun.freeze_time("2016-1-4")
def test_TimeAtAltitude_NoDate(london):
    dt = sun.time_at_elevation(london, 6, direction=SunDirection.RISING)
    cdt = datetime.datetime(2016, 1, 4, 9, 5, 0, tzinfo=pytz.utc)
    # Use error of 5 minutes as website has a rather coarse accuracy
    assert datetime_almost_equal(dt, cdt, 300)


def test_TimeAtAltitude_SunSetting(london):
    d = datetime.date(2016, 1, 4)
    dt = sun.time_at_elevation(london, 14, d, SunDirection.SETTING)
    cdt = datetime.datetime(2016, 1, 4, 13, 20, 0, tzinfo=pytz.utc)
    assert datetime_almost_equal(dt, cdt, 300)


def test_TimeAtAltitude_GreaterThan90(london):
    d = datetime.date(2016, 1, 4)
    dt = sun.time_at_elevation(london, 166, d, SunDirection.RISING)
    cdt = datetime.datetime(2016, 1, 4, 13, 20, 0, tzinfo=pytz.utc)
    assert datetime_almost_equal(dt, cdt, 300)


def test_TimeAtAltitude_GreaterThan180(london):
    d = datetime.date(2015, 12, 1)
    dt = sun.time_at_elevation(london, 186, d, SunDirection.RISING)
    cdt = datetime.datetime(2015, 12, 1, 16, 34, tzinfo=pytz.utc)
    assert datetime_almost_equal(dt, cdt, 300)


def test_TimeAtAltitude_SunRisingBelowHorizon(london):
    d = datetime.date(2016, 1, 4)
    dt = sun.time_at_elevation(london, -18, d, SunDirection.RISING)
    cdt = datetime.datetime(2016, 1, 4, 6, 0, 0, tzinfo=pytz.utc)
    assert datetime_almost_equal(dt, cdt, 300)


def test_TimeAtAltitude_BadElevation(london):
    d = datetime.date(2016, 1, 4)
    with pytest.raises(ValueError):
        sun.time_at_elevation(london, 20, d, SunDirection.RISING)


def test_Daylight(london):
    d = datetime.date(2016, 1, 6)
    start, end = sun.daylight(london, d)
    cstart = datetime.datetime(2016, 1, 6, 8, 5, 0, tzinfo=pytz.utc)
    cend = datetime.datetime(2016, 1, 6, 16, 7, 0, tzinfo=pytz.utc)
    assert datetime_almost_equal(start, cstart, 120)
    assert datetime_almost_equal(end, cend, 120)


@freezegun.freeze_time("2016-1-06")
def test_Daylight_NoDate(london):
    start = pytz.utc.localize(datetime.datetime(2016, 1, 6, 8, 5, 0))
    end = pytz.utc.localize(datetime.datetime(2016, 1, 6, 16, 7, 0))
    ans = sun.daylight(london)
    assert datetime_almost_equal(ans[0], start, 120)
    assert datetime_almost_equal(ans[1], end, 120)


def test_Nighttime(london):
    d = datetime.date(2016, 1, 6)
    start, end = sun.night(london, d)
    cstart = datetime.datetime(2016, 1, 6, 16, 46, tzinfo=pytz.utc)
    cend = datetime.datetime(2016, 1, 7, 7, 25, tzinfo=pytz.utc)
    assert datetime_almost_equal(start, cstart, 120)
    assert datetime_almost_equal(end, cend, 120)


@freezegun.freeze_time("2016-1-06")
def test_Nighttime_NoDate(london):
    start = pytz.utc.localize(datetime.datetime(2016, 1, 6, 16, 46))
    end = pytz.utc.localize(datetime.datetime(2016, 1, 7, 7, 25))
    ans = sun.night(london)
    assert datetime_almost_equal(ans[0], start, 300)
    assert datetime_almost_equal(ans[1], end, 300)
