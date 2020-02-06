# Test data taken from http://www.timeanddate.com/sun/uk/london

from almost_equal import datetime_almost_equal
import pytest
import pytz
import datetime
import freezegun
from astral import sun
from astral.sun import Depression, SunDirection


@pytest.mark.parametrize(
    "day,dawn",
    [
        (datetime.date(2015, 12, 1), datetime.datetime(2015, 12, 1, 7, 4)),
        (datetime.date(2015, 12, 2), datetime.datetime(2015, 12, 2, 7, 5)),
        (datetime.date(2015, 12, 3), datetime.datetime(2015, 12, 3, 7, 6)),
        (datetime.date(2015, 12, 12), datetime.datetime(2015, 12, 12, 7, 16)),
        (datetime.date(2015, 12, 25), datetime.datetime(2015, 12, 25, 7, 25)),
    ],
)
def test_Sun(day, dawn, london):
    dawn = pytz.utc.localize(dawn)
    dawn_utc = sun.sun(london.observer, day)["dawn"]
    assert datetime_almost_equal(dawn, dawn_utc)


@freezegun.freeze_time("2015-12-01")
def test_Sun_NoDate(london):
    ans = pytz.utc.localize(datetime.datetime(2015, 12, 1, 7, 4))
    assert datetime_almost_equal(sun.sun(london.observer)["dawn"], ans)


@pytest.mark.parametrize(
    "day,dawn",
    [
        (datetime.date(2015, 12, 1), datetime.datetime(2015, 12, 1, 7, 4)),
        (datetime.date(2015, 12, 2), datetime.datetime(2015, 12, 2, 7, 5)),
        (datetime.date(2015, 12, 3), datetime.datetime(2015, 12, 3, 7, 6)),
        (datetime.date(2015, 12, 12), datetime.datetime(2015, 12, 12, 7, 16)),
        (datetime.date(2015, 12, 25), datetime.datetime(2015, 12, 25, 7, 25)),
    ],
)
def test_Dawn_Civil(day, dawn, london):
    dawn = pytz.utc.localize(dawn)
    dawn_utc = sun.dawn(london.observer, day, Depression.CIVIL)
    assert datetime_almost_equal(dawn, dawn_utc)


@freezegun.freeze_time("2015-12-01")
def test_Dawn_NoDate(london):
    ans = pytz.utc.localize(datetime.datetime(2015, 12, 1, 7, 4))
    assert datetime_almost_equal(sun.dawn(london.observer), ans)


@pytest.mark.parametrize(
    "day,dawn",
    [
        (datetime.date(2015, 12, 1), datetime.datetime(2015, 12, 1, 6, 22)),
        (datetime.date(2015, 12, 2), datetime.datetime(2015, 12, 2, 6, 23)),
        (datetime.date(2015, 12, 3), datetime.datetime(2015, 12, 3, 6, 24)),
        (datetime.date(2015, 12, 12), datetime.datetime(2015, 12, 12, 6, 33)),
        (datetime.date(2015, 12, 25), datetime.datetime(2015, 12, 25, 6, 41)),
    ],
)
def test_Dawn_Nautical(day, dawn, london):
    dawn = pytz.utc.localize(dawn)
    dawn_utc = sun.dawn(london.observer, day, 12)
    assert datetime_almost_equal(dawn, dawn_utc)


@pytest.mark.parametrize(
    "day,dawn",
    [
        (datetime.date(2015, 12, 1), datetime.datetime(2015, 12, 1, 5, 41)),
        (datetime.date(2015, 12, 2), datetime.datetime(2015, 12, 2, 5, 42)),
        (datetime.date(2015, 12, 3), datetime.datetime(2015, 12, 3, 5, 44)),
        (datetime.date(2015, 12, 12), datetime.datetime(2015, 12, 12, 5, 52)),
        (datetime.date(2015, 12, 25), datetime.datetime(2015, 12, 25, 6, 1)),
    ],
)
def test_Dawn_Astronomical(day, dawn, london):
    dawn = pytz.utc.localize(dawn)
    dawn_utc = sun.dawn(london.observer, day, 18)
    assert datetime_almost_equal(dawn, dawn_utc)


@pytest.mark.parametrize(
    "day,sunrise",
    [
        (datetime.date(2015, 1, 1), datetime.datetime(2015, 1, 1, 8, 6)),
        (datetime.date(2015, 12, 1), datetime.datetime(2015, 12, 1, 7, 43)),
        (datetime.date(2015, 12, 2), datetime.datetime(2015, 12, 2, 7, 45)),
        (datetime.date(2015, 12, 3), datetime.datetime(2015, 12, 3, 7, 46)),
        (datetime.date(2015, 12, 12), datetime.datetime(2015, 12, 12, 7, 56)),
        (datetime.date(2015, 12, 25), datetime.datetime(2015, 12, 25, 8, 5)),
    ],
)
def test_Sunrise(day, sunrise, london):
    sunrise = pytz.utc.localize(sunrise)
    sunrise_utc = sun.sunrise(london.observer, day)
    assert datetime_almost_equal(sunrise, sunrise_utc)


@freezegun.freeze_time("2015-12-01")
def test_Sunrise_NoDate(london):
    ans = pytz.utc.localize(datetime.datetime(2015, 12, 1, 7, 43))
    assert datetime_almost_equal(sun.sunrise(london.observer), ans)


@pytest.mark.parametrize(
    "day,sunset",
    [
        (datetime.date(2015, 1, 1), datetime.datetime(2015, 1, 1, 16, 1)),
        (datetime.date(2015, 12, 1), datetime.datetime(2015, 12, 1, 15, 55)),
        (datetime.date(2015, 12, 2), datetime.datetime(2015, 12, 2, 15, 54)),
        (datetime.date(2015, 12, 3), datetime.datetime(2015, 12, 3, 15, 54)),
        (datetime.date(2015, 12, 12), datetime.datetime(2015, 12, 12, 15, 51)),
        (datetime.date(2015, 12, 25), datetime.datetime(2015, 12, 25, 15, 55)),
    ],
)
def test_Sunset(day, sunset, london):
    sunset = pytz.utc.localize(sunset)
    sunset_utc = sun.sunset(london.observer, day)
    assert datetime_almost_equal(sunset, sunset_utc)


@freezegun.freeze_time("2015-12-01")
def test_Sunset_NoDate(london):
    ans = pytz.utc.localize(datetime.datetime(2015, 12, 1, 15, 55))
    assert datetime_almost_equal(sun.sunset(london.observer), ans)


@pytest.mark.parametrize(
    "day,dusk",
    [
        (datetime.date(2015, 12, 1), datetime.datetime(2015, 12, 1, 16, 34)),
        (datetime.date(2015, 12, 2), datetime.datetime(2015, 12, 2, 16, 34)),
        (datetime.date(2015, 12, 3), datetime.datetime(2015, 12, 3, 16, 33)),
        (datetime.date(2015, 12, 12), datetime.datetime(2015, 12, 12, 16, 31)),
        (datetime.date(2015, 12, 25), datetime.datetime(2015, 12, 25, 16, 36)),
    ],
)
def test_Dusk_Civil(day, dusk, london):
    dusk = pytz.utc.localize(dusk)
    dusk_utc = sun.dusk(london.observer, day)
    assert datetime_almost_equal(dusk, dusk_utc)


@freezegun.freeze_time("2015-12-01")
def test_Dusk_NoDate(london):
    ans = pytz.utc.localize(datetime.datetime(2015, 12, 1, 16, 34))
    assert datetime_almost_equal(sun.dusk(london.observer), ans)


@pytest.mark.parametrize(
    "day,dusk",
    [
        (datetime.date(2015, 12, 1), datetime.datetime(2015, 12, 1, 17, 16)),
        (datetime.date(2015, 12, 2), datetime.datetime(2015, 12, 2, 17, 16)),
        (datetime.date(2015, 12, 3), datetime.datetime(2015, 12, 3, 17, 16)),
        (datetime.date(2015, 12, 12), datetime.datetime(2015, 12, 12, 17, 14)),
        (datetime.date(2015, 12, 25), datetime.datetime(2015, 12, 25, 17, 19)),
    ],
)
def test_Dusk_Nautical(day, dusk, london):
    dusk = pytz.utc.localize(dusk)
    dusk_utc = sun.dusk(london.observer, day, 12)
    assert datetime_almost_equal(dusk, dusk_utc)


@pytest.mark.parametrize(
    "day,noon",
    [
        (datetime.date(2015, 12, 1), datetime.datetime(2015, 12, 1, 11, 49)),
        (datetime.date(2015, 12, 2), datetime.datetime(2015, 12, 2, 11, 49)),
        (datetime.date(2015, 12, 3), datetime.datetime(2015, 12, 3, 11, 50)),
        (datetime.date(2015, 12, 12), datetime.datetime(2015, 12, 12, 11, 54)),
        (datetime.date(2015, 12, 25), datetime.datetime(2015, 12, 25, 12, 00)),
    ],
)
def test_SolarNoon(day, noon, london):
    noon = pytz.utc.localize(noon)
    noon_utc = sun.noon(london.observer, day)
    assert datetime_almost_equal(noon, noon_utc)


@freezegun.freeze_time("2015-12-01")
def test_SolarNoon_NoDate(london):
    ans = pytz.utc.localize(datetime.datetime(2015, 12, 1, 11, 49))
    assert datetime_almost_equal(sun.noon(london), ans)


@pytest.mark.parametrize(
    "day,midnight",
    [
        (datetime.date(2016, 2, 18), datetime.datetime(2016, 2, 18, 0, 14)),
        (datetime.date(2016, 10, 26), datetime.datetime(2016, 10, 25, 23, 44)),
    ],
)
def test_SolarMidnight(day, midnight, london):
    solar_midnight = pytz.utc.localize(midnight)
    solar_midnight_utc = sun.midnight(london.observer, day)
    assert datetime_almost_equal(solar_midnight, solar_midnight_utc)


@freezegun.freeze_time("2016-2-18")
def test_SolarMidnight_NoDate(london):
    ans = pytz.utc.localize(datetime.datetime(2016, 2, 18, 0, 14))
    assert datetime_almost_equal(sun.midnight(london), ans)


@pytest.mark.parametrize(
    "day,twilight",
    [
        (
            datetime.date(2019, 8, 29),
            (
                datetime.datetime(2019, 8, 29, 4, 32),
                datetime.datetime(2019, 8, 29, 5, 7),
            ),
        ),
    ],
)
def test_Twilight_SunRising(day, twilight, london):
    start, end = twilight
    start = pytz.utc.localize(start)
    end = pytz.utc.localize(end)

    info = sun.twilight(london.observer, day)
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
                datetime.datetime(2019, 8, 29, 18, 54),
                datetime.datetime(2019, 8, 29, 19, 30),
            ),
        )
    ],
)
def test_Twilight_SunSetting(day, twilight, london):
    start, end = twilight
    start = pytz.utc.localize(start)
    end = pytz.utc.localize(end)

    info = sun.twilight(london.observer, day, direction=SunDirection.SETTING)
    start_utc = info[0]
    end_utc = info[1]
    assert datetime_almost_equal(start, start_utc)
    assert datetime_almost_equal(end, end_utc)


@freezegun.freeze_time("2019-8-29")
def test_Twilight_NoDate(london):
    start = pytz.utc.localize(datetime.datetime(2019, 8, 29, 18, 54))
    end = pytz.utc.localize(datetime.datetime(2019, 8, 29, 19, 30))
    ans = sun.twilight(london.observer, direction=SunDirection.SETTING)
    assert datetime_almost_equal(ans[0], start)
    assert datetime_almost_equal(ans[1], end)


# Test data from http://www.astroloka.com/rahukaal.aspx?City=Delhi
@pytest.mark.parametrize(
    "day,rahu",
    [
        (
            datetime.date(2015, 12, 1),
            (
                datetime.datetime(2015, 12, 1, 9, 17),
                datetime.datetime(2015, 12, 1, 10, 35),
            ),
        ),
        (
            datetime.date(2015, 12, 2),
            (
                datetime.datetime(2015, 12, 2, 6, 40),
                datetime.datetime(2015, 12, 2, 7, 58),
            ),
        ),
    ],
)
def test_Rahukaalam(day, rahu, new_delhi):
    start, end = rahu
    start = pytz.utc.localize(start)
    end = pytz.utc.localize(end)

    info = sun.rahukaalam(new_delhi.observer, day)
    start_utc = info[0]
    end_utc = info[1]
    assert datetime_almost_equal(start, start_utc)
    assert datetime_almost_equal(end, end_utc)


@freezegun.freeze_time("2015-12-01")
def test_Rahukaalam_NoDate(new_delhi):
    start = pytz.utc.localize(datetime.datetime(2015, 12, 1, 9, 17))
    end = pytz.utc.localize(datetime.datetime(2015, 12, 1, 10, 35))
    ans = sun.rahukaalam(new_delhi.observer)
    assert datetime_almost_equal(ans[0], start)
    assert datetime_almost_equal(ans[1], end)


@pytest.mark.parametrize(
    "dt,angle",
    [
        (datetime.datetime(2015, 12, 14, 11, 0, 0), 14.381311),
        (datetime.datetime(2015, 12, 14, 20, 1, 0), -37.3710156),
    ],
)
def test_SolarAltitude(dt, angle, london):
    assert sun.elevation(london.observer, dt) == pytest.approx(angle, abs=0.001)


@freezegun.freeze_time("2015-12-14 11:00:00", tz_offset=0)
def test_SolarAltitude_NoDate(london):
    assert sun.elevation(london) == pytest.approx(14.381311, abs=0.001)


@pytest.mark.parametrize(
    "dt,angle",
    [
        (datetime.datetime(2015, 12, 14, 11, 0, 0), 166.9676),
        (datetime.datetime(2015, 12, 14, 20, 1, 0), 279.4093),
    ],
)
def test_SolarAzimuth(dt, angle, london):
    assert sun.azimuth(london.observer, dt) == pytest.approx(angle, abs=0.001)


@freezegun.freeze_time("2015-12-14 11:00:00", tz_offset=0)
def test_SolarAzimuth_NoDate(london):
    assert sun.azimuth(london) == pytest.approx(166.9676, abs=0.001)


@pytest.mark.parametrize(
    "dt,angle",
    [
        (datetime.datetime(2019, 8, 29, 14, 34, 0), 46),
        (datetime.datetime(2020, 2, 3, 10, 37, 0), 71),
    ],
)
def test_SolarZenith(dt, angle, london):
    dt = london.tzinfo.localize(dt)
    assert sun.zenith(london.observer, dt) == pytest.approx(angle, abs=0.5)


@freezegun.freeze_time("2019-08-29 14:34:00", tz_offset=1)
def test_SolarZenith_NoDate(london):
    assert sun.zenith(london) == pytest.approx(52.41, abs=0.5)


def test_TimeAtElevation_SunRising(london):
    d = datetime.date(2016, 1, 4)
    dt = sun.time_at_elevation(london.observer, 6, d, SunDirection.RISING)
    cdt = datetime.datetime(2016, 1, 4, 9, 5, 0, tzinfo=pytz.utc)
    # Use error of 5 minutes as website has a rather coarse accuracy
    assert datetime_almost_equal(dt, cdt, 300)


@freezegun.freeze_time("2016-1-4")
def test_TimeAtElevation_NoDate(london):
    dt = sun.time_at_elevation(london.observer, 6, direction=SunDirection.RISING)
    cdt = datetime.datetime(2016, 1, 4, 9, 5, 0, tzinfo=pytz.utc)
    # Use error of 5 minutes as website has a rather coarse accuracy
    assert datetime_almost_equal(dt, cdt, 300)


def test_TimeAtElevation_SunSetting(london):
    d = datetime.date(2016, 1, 4)
    dt = sun.time_at_elevation(london.observer, 14, d, SunDirection.SETTING)
    cdt = datetime.datetime(2016, 1, 4, 13, 20, 0, tzinfo=pytz.utc)
    assert datetime_almost_equal(dt, cdt, 300)


def test_TimeAtElevation_GreaterThan90(london):
    d = datetime.date(2016, 1, 4)
    dt = sun.time_at_elevation(london.observer, 166, d, SunDirection.RISING)
    cdt = datetime.datetime(2016, 1, 4, 13, 20, 0, tzinfo=pytz.utc)
    assert datetime_almost_equal(dt, cdt, 300)


def test_TimeAtElevation_GreaterThan180(london):
    d = datetime.date(2015, 12, 1)
    dt = sun.time_at_elevation(london.observer, 186, d, SunDirection.RISING)
    cdt = datetime.datetime(2015, 12, 1, 16, 34, tzinfo=pytz.utc)
    assert datetime_almost_equal(dt, cdt, 300)


def test_TimeAtElevation_SunRisingBelowHorizon(london):
    d = datetime.date(2016, 1, 4)
    dt = sun.time_at_elevation(london.observer, -18, d, SunDirection.RISING)
    cdt = datetime.datetime(2016, 1, 4, 6, 0, 0, tzinfo=pytz.utc)
    assert datetime_almost_equal(dt, cdt, 300)


def test_TimeAtElevation_BadElevation(london):
    d = datetime.date(2016, 1, 4)
    with pytest.raises(ValueError):
        sun.time_at_elevation(london.observer, 20, d, SunDirection.RISING)


def test_Daylight(london):
    d = datetime.date(2016, 1, 6)
    start, end = sun.daylight(london.observer, d)
    cstart = datetime.datetime(2016, 1, 6, 8, 5, 0, tzinfo=pytz.utc)
    cend = datetime.datetime(2016, 1, 6, 16, 7, 0, tzinfo=pytz.utc)
    assert datetime_almost_equal(start, cstart, 120)
    assert datetime_almost_equal(end, cend, 120)


@freezegun.freeze_time("2016-1-06")
def test_Daylight_NoDate(london):
    start = pytz.utc.localize(datetime.datetime(2016, 1, 6, 8, 5, 0))
    end = pytz.utc.localize(datetime.datetime(2016, 1, 6, 16, 7, 0))
    ans = sun.daylight(london.observer)
    assert datetime_almost_equal(ans[0], start, 120)
    assert datetime_almost_equal(ans[1], end, 120)


def test_Nighttime(london):
    d = datetime.date(2016, 1, 6)
    start, end = sun.night(london.observer, d)
    cstart = datetime.datetime(2016, 1, 6, 16, 46, tzinfo=pytz.utc)
    cend = datetime.datetime(2016, 1, 7, 7, 25, tzinfo=pytz.utc)
    assert datetime_almost_equal(start, cstart, 120)
    assert datetime_almost_equal(end, cend, 120)


@freezegun.freeze_time("2016-1-06")
def test_Nighttime_NoDate(london):
    start = pytz.utc.localize(datetime.datetime(2016, 1, 6, 16, 46))
    end = pytz.utc.localize(datetime.datetime(2016, 1, 7, 7, 25))
    ans = sun.night(london.observer)
    assert datetime_almost_equal(ans[0], start, 300)
    assert datetime_almost_equal(ans[1], end, 300)
