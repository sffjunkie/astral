import datetime
from math import (
    acos,
    asin,
    atan2,
    ceil,
    cos,
    degrees,
    floor,
    fmod,
    radians,
    sin,
    sqrt,
    tan,
)
from typing import Union

import pytz

from astral import SunDirection, AstralError


def proper_angle(value: float) -> float:
    if value > 0.0:
        value /= 360.0
        return (value - floor(value)) * 360.0
    else:
        tmp = ceil(abs(value / 360.0))
        return value + tmp * 360.0


def julianday(
    date: datetime.date
) -> float:
    y = date.year
    m = date.month
    d = date.day

    if m <= 2:
        y -= 1
        m += 12

    a = floor(y / 100)
    b = 2 - a + floor(a / 4)
    jd = floor(365.25 * (y + 4716)) + floor(30.6001 * (m + 1)) + d + b - 1524.5

    return jd


def minutes_to_timedelta(minutes: float) -> datetime.timedelta:
    d = int(minutes / 1440)
    minutes = minutes - (d * 1440)
    minutes = minutes * 60
    s = int(minutes)
    sfrac = minutes - s
    us = int(sfrac * 1_000_000)

    return datetime.timedelta(days=d, seconds=s, microseconds=us)


def jday_to_jcentury(julianday: float) -> float:
    return (julianday - 2451545.0) / 36525.0


def jcentury_to_jday(juliancentury: float) -> float:
    return (juliancentury * 36525.0) + 2451545.0


def geom_mean_long_sun(juliancentury: float) -> float:
    l0 = 280.46646 + juliancentury * (36000.76983 + 0.0003032 * juliancentury)
    return l0 % 360.0


def geom_mean_anomaly_sun(juliancentury: float) -> float:
    return 357.52911 + juliancentury * (35999.05029 - 0.0001537 * juliancentury)


def eccentrilocation_earth_orbit(juliancentury: float) -> float:
    return 0.016708634 - juliancentury * (0.000042037 + 0.0000001267 * juliancentury)


def sun_eq_of_center(juliancentury: float) -> float:
    m = geom_mean_anomaly_sun(juliancentury)

    mrad = radians(m)
    sinm = sin(mrad)
    sin2m = sin(mrad + mrad)
    sin3m = sin(mrad + mrad + mrad)

    c = (
        sinm * (1.914602 - juliancentury * (0.004817 + 0.000014 * juliancentury))
        + sin2m * (0.019993 - 0.000101 * juliancentury)
        + sin3m * 0.000289
    )

    return c


def sun_true_long(juliancentury: float) -> float:
    l0 = geom_mean_long_sun(juliancentury)
    c = sun_eq_of_center(juliancentury)

    return l0 + c


def sun_true_anomoly(juliancentury: float) -> float:
    m = geom_mean_anomaly_sun(juliancentury)
    c = sun_eq_of_center(juliancentury)

    return m + c


def sun_rad_vector(juliancentury: float) -> float:
    v = sun_true_anomoly(juliancentury)
    e = eccentrilocation_earth_orbit(juliancentury)

    return (1.000001018 * (1 - e * e)) / (1 + e * cos(radians(v)))


def sun_apparent_long(juliancentury: float) -> float:
    true_long = sun_true_long(juliancentury)

    omega = 125.04 - 1934.136 * juliancentury
    return true_long - 0.00569 - 0.00478 * sin(radians(omega))


def mean_obliquity_of_ecliptic(juliancentury: float) -> float:
    seconds = 21.448 - juliancentury * (
        46.815 + juliancentury * (0.00059 - juliancentury * (0.001813))
    )
    return 23.0 + (26.0 + (seconds / 60.0)) / 60.0


def obliquity_correction(juliancentury: float) -> float:
    e0 = mean_obliquity_of_ecliptic(juliancentury)

    omega = 125.04 - 1934.136 * juliancentury
    return e0 + 0.00256 * cos(radians(omega))


def sun_rt_ascension(juliancentury: float) -> float:
    oc = obliquity_correction(juliancentury)
    al = sun_apparent_long(juliancentury)

    tananum = cos(radians(oc)) * sin(radians(al))
    tanadenom = cos(radians(al))

    return degrees(atan2(tananum, tanadenom))


def sun_declination(juliancentury: float) -> float:
    e = obliquity_correction(juliancentury)
    lambd = sun_apparent_long(juliancentury)

    sint = sin(radians(e)) * sin(radians(lambd))
    return degrees(asin(sint))


def var_y(juliancentury: float) -> float:
    epsilon = obliquity_correction(juliancentury)
    y = tan(radians(epsilon) / 2.0)
    return y * y


def eq_of_time(juliancentury: float) -> float:
    l0 = geom_mean_long_sun(juliancentury)
    e = eccentrilocation_earth_orbit(juliancentury)
    m = geom_mean_anomaly_sun(juliancentury)

    y = var_y(juliancentury)

    sin2l0 = sin(2.0 * radians(l0))
    sinm = sin(radians(m))
    cos2l0 = cos(2.0 * radians(l0))
    sin4l0 = sin(4.0 * radians(l0))
    sin2m = sin(2.0 * radians(m))

    Etime = (
        y * sin2l0
        - 2.0 * e * sinm
        + 4.0 * e * y * sinm * cos2l0
        - 0.5 * y * y * sin4l0
        - 1.25 * e * e * sin2m
    )

    return degrees(Etime) * 4.0


def hour_angle(
    latitude: float, declination: float, zenith: float, direction: SunDirection
) -> float:
    latitude_rad = radians(latitude)
    declination_rad = radians(declination)
    depression_rad = radians(zenith)

    n = cos(depression_rad)
    d = cos(latitude_rad) * cos(declination_rad)
    t = tan(latitude_rad) * tan(declination_rad)
    h = (n / d) - t

    HA = acos(h)
    if direction == SunDirection.SETTING:
        HA = -HA
    return HA


def adjustment_for_elevation(elevation: float) -> float:
    """Calculate the extra degrees of depression due to the increase in elevation.

    :param elevation: Elevation above the earth in metres
    """

    if elevation <= 0:
        return 0

    r = 6356900  # radius of the earth
    a1 = r
    h1 = r + elevation
    theta1 = acos(a1 / h1)

    a2 = r * sin(theta1)
    b2 = r - (r * cos(theta1))
    h2 = sqrt(pow(a2, 2) + pow(b2, 2))
    alpha = acos(a2 / h2)

    return degrees(alpha)


def time_of_transit(
    observer_latitude: float,
    observer_longitude: float,
    observer_elevation: float,
    date: datetime.date,
    zenith: float,
    direction: SunDirection,
) -> datetime.datetime:
    """Calculate the time when the sun transits the specificed zenith

    :param date: The date to calculate for
    :param observer_latitude: The latitude of the observer
    :param observer_longitude: The longitude of the observer
    :param observer_elevation: The elevation of the observer
    :param zenith: The zenith angle for which to calculate the transit time
    :param direction: The direction that the sun is traversing
    """
    if observer_latitude > 89.8:
        observer_latitude = 89.8

    if observer_latitude < -89.8:
        observer_latitude = -89.8

    adjustment = 0.0
    if observer_elevation > 0:
        adjustment = adjustment_for_elevation(observer_elevation)

    jd = julianday(date)
    t = jday_to_jcentury(jd)
    eqtime = eq_of_time(t)
    solarDec = sun_declination(t)

    hourangle = hour_angle(observer_latitude, solarDec, zenith + adjustment, direction)

    delta = -observer_longitude - degrees(hourangle)
    timeDiff = 4.0 * delta
    timeUTC = 720.0 + timeDiff - eqtime

    t = jday_to_jcentury(jcentury_to_jday(t) + timeUTC / 1440.0)
    eqtime = eq_of_time(t)
    solarDec = sun_declination(t)
    hourangle = hour_angle(observer_latitude, solarDec, zenith + adjustment, direction)

    delta = -observer_longitude - degrees(hourangle)
    timeDiff = 4.0 * delta
    timeUTC = 720 + timeDiff - eqtime

    if timeUTC < 0:
        raise AstralError(f"Sun never transits at a zenith of {zenith} on {date}")

    td = minutes_to_timedelta(timeUTC)
    dt = datetime.datetime(date.year, date.month, date.day) + td
    dt = pytz.utc.localize(dt)  # pylint: disable=E1120
    return dt


def solar_noon(longitude: float, date: datetime.date) -> datetime.datetime:
    """Calculate solar noon time in the UTC timezone.

    :param date:     Date to calculate for.
    :param observer: Observer to calculate noon time for
    :return:         The UTC date and time at which noon occurs.
    """
    jc = jday_to_jcentury(julianday(date))
    eqtime = eq_of_time(jc)
    timeUTC = (720.0 - (4 * longitude) - eqtime) / 60.0

    hour = int(timeUTC)
    minute = int((timeUTC - hour) * 60)
    second = int((((timeUTC - hour) * 60) - minute) * 60)

    if second > 59:
        second -= 60
        minute += 1
    elif second < 0:
        second += 60
        minute -= 1

    if minute > 59:
        minute -= 60
        hour += 1
    elif minute < 0:
        minute += 60
        hour -= 1

    if hour > 23:
        hour -= 24
        date += datetime.timedelta(days=1)
    elif hour < 0:
        hour += 24
        date -= datetime.timedelta(days=1)

    noon = datetime.datetime(date.year, date.month, date.day, hour, minute, second)
    return pytz.utc.localize(noon)  # pylint: disable=E1120


def solar_midnight(longitude: float, date: datetime.date) -> datetime.datetime:
    """Calculate solar midnight time in the UTC timezone.

    Note that this claculates the solar midgnight that is closest
    to 00:00:00 of the specified date i.e. it may return a time that is on
    the previous day.

    :param date:     Date to calculate for.
    :param observer: Observer to calculate solar midnight for
    :return:         The UTC date and time at which midnight occurs.
    """

    jd = julianday(date)
    newt = jday_to_jcentury(jd + 0.5 + -longitude / 360.0)

    eqtime = eq_of_time(newt)
    timeUTC = (-longitude * 4.0) - eqtime

    timeUTC = timeUTC / 60.0
    hour = int(timeUTC)
    minute = int((timeUTC - hour) * 60)
    second = int((((timeUTC - hour) * 60) - minute) * 60)

    if second > 59:
        second -= 60
        minute += 1
    elif second < 0:
        second += 60
        minute -= 1

    if minute > 59:
        minute -= 60
        hour += 1
    elif minute < 0:
        minute += 60
        hour -= 1

    if hour < 0:
        hour += 24
        date -= datetime.timedelta(days=1)

    midnight = datetime.datetime(date.year, date.month, date.day, hour, minute, second)
    return pytz.utc.localize(midnight)  # pylint: disable=E1120


def _zenith_and_azimuth():
    pass


def zenith(dateandtime: datetime.datetime, latitude: float, longitude: float) -> float:
    """Calculate the elevation angle of the sun.

    :param dateandtime: The date and time for which to calculate the angle.
    :param observer:    The Observer to calculate the solar elevation for
    :return:            The elevation angle in degrees above the horizon.

    If `dateandtime` is a naive Python datetime then it is assumed to be
    in the UTC timezone.
    """

    if latitude > 89.8:
        latitude = 89.8

    if latitude < -89.8:
        latitude = -89.8

    if dateandtime.tzinfo is None:
        timezone_hour_offset = 0.0
        utc_datetime = pytz.utc.localize(dateandtime)
    else:
        timezone_hour_offset = -dateandtime.utcoffset().total_seconds() / 3600.0
        utc_datetime = dateandtime.astimezone(pytz.utc)

    day_fraction = (
        utc_datetime.hour + (utc_datetime.minute / 60.0) + (utc_datetime.second / 3600)
    ) / 24.0

    JD = julianday(dateandtime)
    t = jday_to_jcentury(JD + day_fraction)
    solarDec = sun_declination(t)
    eqtime = eq_of_time(t)

    solarTimeFix = eqtime - (4.0 * -longitude) + (60 * timezone_hour_offset)
    trueSolarTime = (
        dateandtime.hour * 60.0
        + dateandtime.minute
        + dateandtime.second / 60.0
        + solarTimeFix
    )
    #    in minutes as a float, fractional part is seconds

    if trueSolarTime > 1440:
        trueSolarTime = fmod(trueSolarTime, 1440)

    hourangle = trueSolarTime / 4.0 - 180.0
    # Thanks to Louis Schwarzmayr for the next line:
    if hourangle < -180:
        hourangle = hourangle + 360.0

    harad = radians(hourangle)

    csz = sin(radians(latitude)) * sin(radians(solarDec)) + cos(
        radians(latitude)
    ) * cos(radians(solarDec)) * cos(harad)

    if csz > 1.0:
        csz = 1.0
    elif csz < -1.0:
        csz = -1.0

    zenith = degrees(acos(csz))
    return zenith

    # Correct for refraction
    # exoatmElevation = 90.0 - zenith

    # if exoatmElevation <= 85.0:
    #     te = tan(radians(exoatmElevation))
    #     if exoatmElevation > 5.0:
    #         refractionCorrection = (
    #             58.1 / te - 0.07 / (te * te * te) + 0.000086 / (te * te * te * te * te)
    #         )
    #     elif exoatmElevation > -0.575:
    #         step1 = -12.79 + exoatmElevation * 0.711
    #         step2 = 103.4 + exoatmElevation * (step1)
    #         step3 = -518.2 + exoatmElevation * (step2)
    #         refractionCorrection = 1735.0 + exoatmElevation * (step3)
    #     else:
    #         refractionCorrection = -20.774 / te

    #     refractionCorrection = refractionCorrection / 3600.0
    #     zenith -= refractionCorrection

    # return zenith


def azimuth(dateandtime: datetime.datetime, latitude: float, longitude: float) -> float:
    """Calculate the azimuth angle of the sun.

    :param dateandtime: The date and time for which to calculate the angle.
    :param observer:    The Observer to calculate the solar azimuth for
    :return:            The azimuth angle in degrees clockwise from North.

    If `dateandtime` is a naive Python datetime then it is assumed to be
    in the UTC timezone.
    """

    if latitude > 89.8:
        latitude = 89.8

    if latitude < -89.8:
        latitude = -89.8

    if dateandtime.tzinfo is None:
        zone = 0.0
        utc_datetime = dateandtime
    else:
        zone = -dateandtime.utcoffset().total_seconds() / 3600.0
        utc_datetime = dateandtime.astimezone(pytz.utc)

    timenow = (
        utc_datetime.hour
        + (utc_datetime.minute / 60.0)
        + (utc_datetime.second / 3600.0)
    )

    JD = julianday(dateandtime)
    t = jday_to_jcentury(JD + timenow / 24.0)
    solarDec = sun_declination(t)
    eqtime = eq_of_time(t)

    solarTimeFix = eqtime - (4.0 * -longitude) + (60 * zone)
    trueSolarTime = (
        dateandtime.hour * 60.0
        + dateandtime.minute
        + dateandtime.second / 60.0
        + solarTimeFix
    )
    #    in minutes as a float, fractional part is seconds

    while trueSolarTime > 1440:
        trueSolarTime = trueSolarTime - 1440

    hourangle = trueSolarTime / 4.0 - 180.0
    #    Thanks to Louis Schwarzmayr for the next line:
    if hourangle < -180:
        hourangle = hourangle + 360.0

    harad = radians(hourangle)

    csz = sin(radians(latitude)) * sin(radians(solarDec)) + cos(
        radians(latitude)
    ) * cos(radians(solarDec)) * cos(harad)

    if csz > 1.0:
        csz = 1.0
    elif csz < -1.0:
        csz = -1.0

    zenith = degrees(acos(csz))

    azDenom = cos(radians(latitude)) * sin(radians(zenith))

    if abs(azDenom) > 0.001:
        azRad = (
            (sin(radians(latitude)) * cos(radians(zenith))) - sin(radians(solarDec))
        ) / azDenom

        if abs(azRad) > 1.0:
            if azRad < 0:
                azRad = -1.0
            else:
                azRad = 1.0

        azimuth = 180.0 - degrees(acos(azRad))

        if hourangle > 0.0:
            azimuth = -azimuth
    else:
        if latitude > 0.0:
            azimuth = 180.0
        else:
            azimuth = 0.0

    if azimuth < 0.0:
        azimuth = azimuth + 360.0

    return azimuth


def altitude(
    dateandtime: datetime.datetime, latitude: float, longitude: float
) -> float:
    return 90 - zenith(dateandtime, latitude, longitude)
