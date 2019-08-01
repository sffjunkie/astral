import datetime

import pytz
from pytest import approx

from astral.sun import calc


def test_JulianDay():
    test_data = [
        (datetime.date(2012, 1, 1), 2455927.5),
        (datetime.date(2013, 1, 1), 2456293.5),
        (datetime.date(2013, 6, 1), 2456444.5),
        (datetime.date(1867, 2, 1), 2402998.5),
        (datetime.date(3200, 11, 14), 2890153.5),
    ]

    for d, jd in test_data:
        assert calc.julianday(d) == jd


def test_JulianCentury():
    test_data = [
        (2455927.5, 0.119986311),
        (2456293.5, 0.130006845),
        (2456444.5, 0.134140999),
        (2402998.5, -1.329130732),
        (2890153.5, 12.00844627),
    ]

    for jd, jc in test_data:
        assert approx(calc.jday_to_jcentury(jd), jc)


def test_JulianCenturyToJulianDay():
    test_data = [
        (0.119986311, 2455927.5),
        (0.130006845, 2456293.5),
        (0.134140999, 2456444.5),
        (-1.329130732, 2402998.5),
        (12.00844627, 2890153.5),
    ]

    for jc, jd in test_data:
        assert approx(calc.jcentury_to_jday(jc), jd)


def test_GeomMeanLongSun():
    test_data = [
        (-1.329130732, 310.7374254),
        (12.00844627, 233.8203529),
        (0.184134155, 69.43779106),
    ]

    for jc, gmls in test_data:
        assert approx(calc.geom_mean_long_sun(jc), gmls)


def test_GeomAnomolyLongSun():
    test_data = [
        (0.119986311, 4676.922342),
        (12.00844627, 432650.1681),
        (0.184134155, 6986.1838),
    ]

    for jc, gmas in test_data:
        assert approx(calc.geom_mean_anomaly_sun(jc), gmas)


def test_EccentricityEarthOrbit():
    test_data = [
        (0.119986311, 0.016703588),
        (12.00844627, 0.016185564),
        (0.184134155, 0.016700889),
    ]

    for jc, eeo in test_data:
        assert approx(calc.eccentrilocation_earth_orbit(jc), eeo, abs=1e-6)


def test_SunEqOfCenter():
    test_data = [
        (0.119986311, -0.104951648),
        (12.00844627, -1.753028843),
        (0.184134155, 1.046852316),
    ]

    for jc, eos in test_data:
        assert approx(calc.sun_eq_of_center(jc), eos, abs=1e-6)


def test_SunTrueLong():
    test_data = [
        (0.119986311, 279.9610686),
        (12.00844627, 232.0673241),
        (0.184134155, 70.48464338),
    ]

    for jc, stl in test_data:
        assert approx(calc.sun_true_long(jc), stl, abs=1e-6)


def test_SunTrueAnomaly():
    test_data = [
        (0.119986311, 4676.817391),
        (12.00844627, 432648.4151),
        (0.184134155, 6987.230652),
    ]

    for jc, sta in test_data:
        assert approx(calc.sun_true_anomoly(jc), sta, abs=1e-3)


def test_SunRadVector():
    test_data = [
        (0.119986311, 0.983322329),
        (12.00844627, 0.994653382),
        (0.184134155, 1.013961204),
    ]

    for jc, srv in test_data:
        assert approx(calc.sun_rad_vector(jc), srv, abs=1e-6)


def test_SunApparentLong():
    test_data = [
        (0.119986311, 279.959949),
        (12.00844627, 232.0658118),
        (0.184134155, 70.47523335),
    ]

    for jc, sal in test_data:
        assert approx(calc.sun_apparent_long(jc), sal, abs=1e-5)


def test_MeanObliquityOfEcliptic():
    test_data = [
        (0.119986311, 23.43773079),
        (12.00844627, 23.28397972),
        (0.184134155, 23.4368966),
    ]

    for jc, mooe in test_data:
        assert approx(calc.mean_obliquity_of_ecliptic(jc), mooe, abs=1e-6)


def test_ObliquityCorrection():
    test_data = [
        (0.119986311, 23.43773079),
        (12.00844627, 23.28397972),
        (0.184134155, 23.4368966),
    ]

    for jc, oc in test_data:
        assert approx(calc.obliquity_correction(jc), oc, abs=1e-5)


def test_SunRtAscension():
    test_data = [
        (0.119986311, -79.16480352),
        (12.00844627, -130.3163904),
        (0.184134155, 68.86915896),
    ]

    for jc, sra in test_data:
        assert approx(calc.sun_rt_ascension(jc), sra, abs=1e-7)


def test_SunDeclination():
    test_data = [
        (0.119986311, -23.06317068),
        (12.00844627, -18.16694394),
        (0.184134155, 22.01463552),
    ]

    for jc, sd in test_data:
        assert approx(calc.sun_declination(jc), sd, abs=1e-6)


def test_EquationOfTime():
    test_data = [
        (0.119986311, -3.078190421),
        (12.00844627, 16.58348133),
        (0.184134155, 2.232039737),
    ]

    for jc, eot in test_data:
        assert approx(calc.eq_of_time(jc), eot, abs=1e-6)


def test_HourAngle(london):
    test_data = [
        (datetime.date(2012, 1, 1), 1.03555238),
        (datetime.date(3200, 11, 14), 1.172253118),
        (datetime.date(2018, 6, 1), 2.133712555),
    ]

    for d, ha in test_data:
        jd = calc.julianday(d)
        jc = calc.jday_to_jcentury(jd)
        decl = calc.sun_declination(jc)

        assert approx(
            calc.hour_angle(
                london.latitude, decl, 90.8333, calc.SunDirection.RISING
            ),
            ha,
            abs=1e-6,
        )


def test_ProperAngle():
    assert approx(calc.proper_angle(12), 12)
    assert approx(calc.proper_angle(13.3), 13.3)
    assert approx(calc.proper_angle(-3), 357)
    assert approx(calc.proper_angle(363), 3)


def test_Azimuth(new_delhi):
    d = datetime.datetime(2001, 6, 21, 13, 11, 0)
    assert approx(
        calc.azimuth(d, new_delhi.latitude, new_delhi.longitude),
        292.77,
    )


def test_Altitude(new_delhi):
    d = datetime.datetime(2001, 6, 21, 13, 11, 0)
    assert approx(
        calc.altitude(d, new_delhi.latitude, new_delhi.longitude),
        7.41,
    )


def test_Altitude_NonNaive(new_delhi):
    d = datetime.datetime(2001, 6, 21, 18, 41, 0)
    d = new_delhi.tz.localize(d)
    assert approx(
        calc.altitude(d, new_delhi.latitude, new_delhi.longitude),
        7.41,
    )


def test_Azimuth_Above85Degrees():
    d = datetime.datetime(2001, 6, 21, 13, 11, 0)
    assert approx(calc.azimuth(d, 86, 77.2), 276.23)


def test_Altitude_Above85Degrees():
    d = datetime.datetime(2001, 6, 21, 13, 11, 0)
    assert approx(calc.altitude(d, 86, 77.2), 23.10)
