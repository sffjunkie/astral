import datetime

import freezegun
import pytest

from astral import Observer, sun, today
from astral.location import Location


@pytest.mark.parametrize(
    "jc,gmls",
    [
        (-1.329130732, 310.7374254),
        (12.00844627, 233.8203529),
        (0.184134155, 69.43779106),
    ],
)
def test_GeomMeanLongSun(jc: float, gmls: float):
    assert sun.geom_mean_long_sun(jc) == pytest.approx(gmls)  # type: ignore


@pytest.mark.parametrize(
    "jc,gmas",
    [
        (0.119986311, 4676.922342),
        (12.00844627, 432650.1681),
        (0.184134155, 6986.1838),
    ],
)
def test_GeomAnomolyLongSun(jc: float, gmas: float):
    assert sun.geom_mean_anomaly_sun(jc) == pytest.approx(gmas)  # type: ignore


@pytest.mark.parametrize(
    "jc,eeo",
    [
        (0.119986311, 0.016703588),
        (12.00844627, 0.016185564),
        (0.184134155, 0.016700889),
    ],
)
def test_EccentricityEarthOrbit(jc: float, eeo: float):
    assert sun.eccentric_location_earth_orbit(jc) == pytest.approx(eeo, abs=1e-6)  # type: ignore


@pytest.mark.parametrize(
    "jc,eos",
    [
        (0.119986311, -0.104951648),
        (12.00844627, -1.753028843),
        (0.184134155, 1.046852316),
    ],
)
def test_SunEqOfCenter(jc: float, eos: float):
    assert sun.sun_eq_of_center(jc) == pytest.approx(eos, abs=1e-6)  # type: ignore


@pytest.mark.parametrize(
    "jc,stl",
    [
        (0.119986311, 279.9610686),
        (12.00844627, 232.0673358),
        (0.184134155, 70.48465428),
    ],
)
def test_SunTrueLong(jc: float, stl: float):
    assert sun.sun_true_long(jc) == pytest.approx(stl, abs=0.001)  # type: ignore


@pytest.mark.parametrize(
    "jc,sta",
    [
        (0.119986311, 4676.817391),
        (12.00844627, 432648.4151),
        (0.184134155, 6987.230663),
    ],
)
def test_SunTrueAnomaly(jc: float, sta: float):
    assert sun.sun_true_anomoly(jc) == pytest.approx(sta, abs=0.001)  # type: ignore


@pytest.mark.parametrize(
    "jc,srv",
    [
        (0.119986311, 0.983322329),
        (12.00844627, 0.994653382),
        (0.184134155, 1.013961204),
    ],
)
def test_SunRadVector(jc: float, srv: float):
    assert sun.sun_rad_vector(jc) == pytest.approx(srv, abs=0.001)  # type: ignore


@pytest.mark.parametrize(
    "jc,sal",
    [
        (0.119986311, 279.95995849827),
        (12.00844627, 232.065823531804),
        (0.184134155, 70.475244256027),
    ],
)
def test_SunApparentLong(jc: float, sal: float):
    assert sun.sun_apparent_long(jc) == pytest.approx(sal)  # type: ignore


@pytest.mark.parametrize(
    "jc,mooe",
    [
        (0.119986311, 23.4377307876356),
        (12.00844627, 23.2839797200388),
        (0.184134155, 23.4368965974579),
    ],
)
def test_MeanObliquityOfEcliptic(jc: float, mooe: float):
    assert sun.mean_obliquity_of_ecliptic(jc) == pytest.approx(mooe)  # type: ignore


@pytest.mark.parametrize(
    "jc,oc",
    [
        (0.119986311, 23.4369810410121),
        (12.00844627, 23.2852236361575),
        (0.184134155, 23.4352890293474),
    ],
)
def test_ObliquityCorrection(jc: float, oc: float):
    assert sun.obliquity_correction(jc) == pytest.approx(oc, abs=0.001)  # type: ignore


@pytest.mark.parametrize(
    "jc,sra",
    [
        (0.119986311, -79.16480352),
        (12.00844627, -130.3163904),
        (0.184134155, 68.86915896),
    ],
)
def test_SunRtAscension(jc: float, sra: float):
    assert sun.sun_rt_ascension(jc) == pytest.approx(sra, abs=0.001)  # type: ignore


@pytest.mark.parametrize(
    "jc,sd",
    [
        (0.119986311, -23.06317068),
        (12.00844627, -18.16694394),
        (0.184134155, 22.01463552),
    ],
)
def test_SunDeclination(jc: float, sd: float):
    assert sun.sun_declination(jc) == pytest.approx(sd, abs=0.001)  # type: ignore


@pytest.mark.parametrize(
    "jc,eot",
    [
        (0.119986311, -3.078194825),
        (12.00844627, 16.58348133),
        (0.184134155, 2.232039737),
    ],
)
def test_EquationOfTime(jc: float, eot: float):
    assert sun.eq_of_time(jc) == pytest.approx(eot)  # type: ignore


@pytest.mark.parametrize(
    "d,ha",
    [
        (datetime.date(2012, 1, 1), 1.03555238),
        (datetime.date(3200, 11, 14), 1.172253118),
        (datetime.date(2018, 6, 1), 2.133712555),
    ],
)
def test_HourAngle(d: datetime.date, ha: float, london: Location):
    midday = datetime.time(12, 0, 0)
    jd = sun.julianday(datetime.datetime.combine(d, midday))
    jc = sun.julianday_to_juliancentury(jd)
    decl = sun.sun_declination(jc)

    assert sun.hour_angle(
        london.latitude, decl, 90.8333, sun.SunDirection.RISING
    ) == pytest.approx(  # type: ignore
        ha, abs=0.1
    )


def test_Azimuth(new_delhi: Location):
    d = datetime.datetime(2001, 6, 21, 13, 11, 0)
    assert sun.azimuth(new_delhi.observer, d) == pytest.approx(292.76, abs=0.1)  # type: ignore


def test_Elevation(new_delhi: Location):
    d = datetime.datetime(2001, 6, 21, 13, 11, 0)
    assert sun.elevation(new_delhi.observer, d) == pytest.approx(7.41, abs=0.1)  # type: ignore


def test_Elevation_NonNaive(new_delhi: Location):
    d = datetime.datetime(2001, 6, 21, 18, 41, 0, tzinfo=new_delhi.tz)
    assert sun.elevation(new_delhi.observer, d) == pytest.approx(7.41, abs=0.1)  # type: ignore


def test_Elevation_WithoutRefraction(new_delhi: Location):
    d = datetime.datetime(2001, 6, 21, 13, 11, 0)
    assert sun.elevation(new_delhi.observer, d, with_refraction=False) == pytest.approx(  # type: ignore
        7.29, abs=0.1
    )


def test_Azimuth_Above85Degrees():
    d = datetime.datetime(2001, 6, 21, 13, 11, 0)
    assert sun.azimuth(Observer(86, 77.2), d) == pytest.approx(276.21, abs=0.1)  # type: ignore


def test_Elevation_Above85Degrees():
    d = datetime.datetime(2001, 6, 21, 13, 11, 0)
    assert sun.elevation(Observer(86, 77.2), d) == pytest.approx(  # type: ignore
        23.102501151619506, abs=0.001
    )


@pytest.mark.parametrize("elevation", range(1, 20))
@freezegun.freeze_time("2020-02-06")
def test_ElevationEqualsTimeAtElevation(elevation: float, london: Location):
    o = london.observer
    td = today()
    et = sun.time_at_elevation(o, elevation, td, with_refraction=True)
    sun_elevation = sun.elevation(o, et, with_refraction=True)
    assert sun_elevation == pytest.approx(elevation, abs=0.1)  # type: ignore
