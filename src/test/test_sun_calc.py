import datetime

import pytest

from astral import sun, Observer


@pytest.mark.parametrize(
    "day,jd",
    [
        (datetime.date(2012, 1, 1), 2455927.5),
        (datetime.date(2013, 1, 1), 2456293.5),
        (datetime.date(2013, 6, 1), 2456444.5),
        (datetime.date(1867, 2, 1), 2402998.5),
        (datetime.date(3200, 11, 14), 2890153.5),
    ],
)
def test_JulianDay(day: datetime.date, jd: float):
    assert sun.julianday(day) == jd


@pytest.mark.parametrize(
    "jd,jc",
    [
        (2455927.5, 0.119986311),
        (2456293.5, 0.130006845),
        (2456444.5, 0.134140999),
        (2402998.5, -1.329130732),
        (2890153.5, 12.00844627),
    ],
)
def test_JulianCentury(jd: float, jc: float):
    assert pytest.approx(sun.jday_to_jcentury(jd), jc)


@pytest.mark.parametrize(
    "jc,jd",
    [
        (0.119986311, 2455927.5),
        (0.130006845, 2456293.5),
        (0.134140999, 2456444.5),
        (-1.329130732, 2402998.5),
        (12.00844627, 2890153.5),
    ],
)
def test_JulianCenturyToJulianDay(jc: float, jd: float):
    assert pytest.approx(sun.jcentury_to_jday(jc), jd)


@pytest.mark.parametrize(
    "jc,gmls",
    [
        (-1.329130732, 310.7374254),
        (12.00844627, 233.8203529),
        (0.184134155, 69.43779106),
    ],
)
def test_GeomMeanLongSun(jc: float, gmls: float):
    assert pytest.approx(sun.geom_mean_long_sun(jc), gmls)


@pytest.mark.parametrize(
    "jc,gmas",
    [(0.119986311, 4676.922342), (12.00844627, 432650.1681), (0.184134155, 6986.1838),],
)
def test_GeomAnomolyLongSun(jc: float, gmas: float):
    assert pytest.approx(sun.geom_mean_anomaly_sun(jc), gmas)


@pytest.mark.parametrize(
    "jc,eeo",
    [
        (0.119986311, 0.016703588),
        (12.00844627, 0.016185564),
        (0.184134155, 0.016700889),
    ],
)
def test_EccentricityEarthOrbit(jc: float, eeo: float):
    assert pytest.approx(sun.eccentric_location_earth_orbit(jc), eeo, abs=1e-6)


@pytest.mark.parametrize(
    "jc,eos",
    [
        (0.119986311, -0.104951648),
        (12.00844627, -1.753028843),
        (0.184134155, 1.046852316),
    ],
)
def test_SunEqOfCenter(jc: float, eos: float):
    assert pytest.approx(sun.sun_eq_of_center(jc), eos, abs=1e-6)


@pytest.mark.parametrize(
    "jc,stl",
    [
        (0.119986311, 279.9610686),
        (12.00844627, 232.0673241),
        (0.184134155, 70.48464338),
    ],
)
def test_SunTrueLong(jc: float, stl: float):
    assert pytest.approx(sun.sun_true_long(jc), stl, abs=1e-6)


@pytest.mark.parametrize(
    "jc,sta",
    [
        (0.119986311, 4676.817391),
        (12.00844627, 432648.4151),
        (0.184134155, 6987.230652),
    ],
)
def test_SunTrueAnomaly(jc: float, sta: float):
    assert pytest.approx(sun.sun_true_anomoly(jc), sta, abs=1e-3)


@pytest.mark.parametrize(
    "jc,srv",
    [
        (0.119986311, 0.983322329),
        (12.00844627, 0.994653382),
        (0.184134155, 1.013961204),
    ],
)
def test_SunRadVector(jc: float, srv: float):
    assert pytest.approx(sun.sun_rad_vector(jc), srv, abs=1e-6)


@pytest.mark.parametrize(
    "jc,sal",
    [
        (0.119986311, 279.959949),
        (12.00844627, 232.0658118),
        (0.184134155, 70.47523335),
    ],
)
def test_SunApparentLong(jc: float, sal: float):
    assert pytest.approx(sun.sun_apparent_long(jc), sal, abs=1e-5)


@pytest.mark.parametrize(
    "jc,mooe",
    [
        (0.119986311, 23.43773079),
        (12.00844627, 23.28397972),
        (0.184134155, 23.4368966),
    ],
)
def test_MeanObliquityOfEcliptic(jc: float, mooe: float):
    assert pytest.approx(sun.mean_obliquity_of_ecliptic(jc), mooe, abs=1e-6)


@pytest.mark.parametrize(
    "jc,oc",
    [
        (0.119986311, 23.43773079),
        (12.00844627, 23.28397972),
        (0.184134155, 23.4368966),
    ],
)
def test_ObliquityCorrection(jc: float, oc: float):
    assert pytest.approx(sun.obliquity_correction(jc), oc, abs=1e-5)


@pytest.mark.parametrize(
    "jc,sra",
    [
        (0.119986311, -79.16480352),
        (12.00844627, -130.3163904),
        (0.184134155, 68.86915896),
    ],
)
def test_SunRtAscension(jc: float, sra: float):
    assert pytest.approx(sun.sun_rt_ascension(jc), sra, abs=1e-7)


@pytest.mark.parametrize(
    "jc,sd",
    [
        (0.119986311, -23.06317068),
        (12.00844627, -18.16694394),
        (0.184134155, 22.01463552),
    ],
)
def test_SunDeclination(jc: float, sd: float):
    assert pytest.approx(sun.sun_declination(jc), sd, abs=1e-6)


@pytest.mark.parametrize(
    "jc,eot",
    [
        (0.119986311, -3.078190421),
        (12.00844627, 16.58348133),
        (0.184134155, 2.232039737),
    ],
)
def test_EquationOfTime(jc: float, eot: float):
    assert pytest.approx(sun.eq_of_time(jc), eot, abs=1e-6)


@pytest.mark.parametrize(
    "d,ha",
    [
        (datetime.date(2012, 1, 1), 1.03555238),
        (datetime.date(3200, 11, 14), 1.172253118),
        (datetime.date(2018, 6, 1), 2.133712555),
    ],
)
def test_HourAngle(d: datetime.date, ha: float, london):
    jd = sun.julianday(d)
    jc = sun.jday_to_jcentury(jd)
    decl = sun.sun_declination(jc)

    assert pytest.approx(
        sun.hour_angle(london.latitude, decl, 90.8333, sun.SunDirection.RISING),
        ha,
        abs=1e-6,
    )


@pytest.mark.parametrize("in_,out", [(12, 12), (13.3, 13.3), (-3, 357), (363, 3)])
def test_ProperAngle(in_, out):
    assert pytest.approx(sun.proper_angle(in_), out)


def test_Azimuth(new_delhi):
    d = datetime.datetime(2001, 6, 21, 13, 11, 0)
    assert pytest.approx(sun.azimuth(new_delhi, d), 292.77,)


def test_Altitude(new_delhi):
    d = datetime.datetime(2001, 6, 21, 13, 11, 0)
    assert pytest.approx(sun.azimuth(new_delhi, d), 7.41,)


def test_Altitude_NonNaive(new_delhi):
    d = datetime.datetime(2001, 6, 21, 18, 41, 0)
    d = new_delhi.tz.localize(d)
    assert pytest.approx(sun.elevation(new_delhi, d), 7.41,)


def test_Azimuth_Above85Degrees():
    d = datetime.datetime(2001, 6, 21, 13, 11, 0)
    assert pytest.approx(sun.azimuth(Observer(86, 77.2), d), 276.23)


def test_Altitude_Above85Degrees():
    d = datetime.datetime(2001, 6, 21, 13, 11, 0)
    assert pytest.approx(sun.elevation(Observer(86, 77.2), d), 23.10)
