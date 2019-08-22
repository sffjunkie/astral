import datetime
from math import (acos, asin, atan2, ceil, cos, degrees, floor, fmod, radians,
                  sin, sqrt, tan)
from typing import Dict, Optional, Tuple

import pytz

from astral import AstralError, Observer, SunDirection, today

__all__ = [
    "solar_noon",
    "solar_midnight",
    "zenith",
    "azimuth",
    "altitude",
    "dawn",
    "sunrise",
    "sunset",
    "dusk",
    "daylight",
    "night",
    "time_at_altitude",
    "twilight",
    "golden_hour",
    "blue_hour",
    "rahukaalam",
]


def proper_angle(value: float) -> float:
    if value > 0.0:
        value /= 360.0
        return (value - floor(value)) * 360.0
    else:
        tmp = ceil(abs(value / 360.0))
        return value + tmp * 360.0


def julianday(date: datetime.date) -> float:
    """Calculate the Julian Day for the specified date"""
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
    """Convert a floating point number of minutes to a :class:`~datetime.timedelta`"""
    d = int(minutes / 1440)
    minutes = minutes - (d * 1440)
    minutes = minutes * 60
    s = int(minutes)
    sfrac = minutes - s
    us = int(sfrac * 1_000_000)

    return datetime.timedelta(days=d, seconds=s, microseconds=us)


def jday_to_jcentury(julianday: float) -> float:
    """Convert a Julian Day number to a Julian Century"""
    return (julianday - 2451545.0) / 36525.0


def jcentury_to_jday(juliancentury: float) -> float:
    """Convert a Julian Century number to a Julian Day"""
    return (juliancentury * 36525.0) + 2451545.0


def geom_mean_long_sun(juliancentury: float) -> float:
    """Calculate the geometric mean longitude of the sun"""
    l0 = 280.46646 + juliancentury * (36000.76983 + 0.0003032 * juliancentury)
    return l0 % 360.0


def geom_mean_anomaly_sun(juliancentury: float) -> float:
    """Calculate the geometric mean anomaly of the sun"""
    return 357.52911 + juliancentury * (35999.05029 - 0.0001537 * juliancentury)


def eccentric_location_earth_orbit(juliancentury: float) -> float:
    """Calculate the eccentricity of Earth's orbit"""
    return 0.016708634 - juliancentury * (0.000042037 + 0.0000001267 * juliancentury)


def sun_eq_of_center(juliancentury: float) -> float:
    """Calculate the equation of the center of the sun"""
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
    """Calculate the sun's true longitude"""
    l0 = geom_mean_long_sun(juliancentury)
    c = sun_eq_of_center(juliancentury)

    return l0 + c


def sun_true_anomoly(juliancentury: float) -> float:
    """Calculate the sun's true anomaly"""
    m = geom_mean_anomaly_sun(juliancentury)
    c = sun_eq_of_center(juliancentury)

    return m + c


def sun_rad_vector(juliancentury: float) -> float:
    v = sun_true_anomoly(juliancentury)
    e = eccentric_location_earth_orbit(juliancentury)

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
    """Calculate the sun's right ascension"""
    oc = obliquity_correction(juliancentury)
    al = sun_apparent_long(juliancentury)

    tananum = cos(radians(oc)) * sin(radians(al))
    tanadenom = cos(radians(al))

    return degrees(atan2(tananum, tanadenom))


def sun_declination(juliancentury: float) -> float:
    """Calculate the sun's declination"""
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
    e = eccentric_location_earth_orbit(juliancentury)
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
    observer: Observer, date: datetime.date, zenith: float, direction: SunDirection
) -> datetime.datetime:
    """Calculate the time in the UTC timezone when the sun transits the specificed zenith

    :param observer: An observer viewing the sun at a specific, latitude, longitude and elevation
    :param date: The date to calculate for
    :param zenith: The zenith angle for which to calculate the transit time
    :param direction: The direction that the sun is traversing
    """
    if observer.latitude > 89.8:
        latitude = 89.8
    elif observer.latitude < -89.8:
        latitude = -89.8
    else:
        latitude = observer.latitude

    adjustment = 0.0
    if observer.elevation > 0:
        adjustment = adjustment_for_elevation(observer.elevation)

    jd = julianday(date)
    t = jday_to_jcentury(jd)
    eqtime = eq_of_time(t)
    solarDec = sun_declination(t)

    hourangle = hour_angle(latitude, solarDec, zenith + adjustment, direction)

    delta = -observer.longitude - degrees(hourangle)
    timeDiff = 4.0 * delta
    timeUTC = 720.0 + timeDiff - eqtime

    t = jday_to_jcentury(jcentury_to_jday(t) + timeUTC / 1440.0)
    eqtime = eq_of_time(t)
    solarDec = sun_declination(t)
    hourangle = hour_angle(latitude, solarDec, zenith + adjustment, direction)

    delta = -observer.longitude - degrees(hourangle)
    timeDiff = 4.0 * delta
    timeUTC = 720 + timeDiff - eqtime

    if timeUTC < 0:
        raise AstralError(f"Sun never transits at a zenith of {zenith} on {date}")

    td = minutes_to_timedelta(timeUTC)
    dt = datetime.datetime(date.year, date.month, date.day) + td
    dt = pytz.utc.localize(dt)  # pylint: disable=E1120
    return dt


def solar_noon(
    observer: Observer,
    date: Optional[datetime.date] = None,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> datetime.datetime:
    """Calculate solar noon time in the UTC timezone.

    :param observer: An observer viewing the sun at a specific, latitude, longitude and elevation
    :param date:     Date to calculate for.
    :return:         The UTC date and time at which noon occurs.
    """
    if date is None:
        date = today(tzinfo)

    jc = jday_to_jcentury(julianday(date))
    eqtime = eq_of_time(jc)
    timeUTC = (720.0 - (4 * observer.longitude) - eqtime) / 60.0

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


def solar_midnight(
    observer: Observer,
    date: Optional[datetime.date] = None,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> datetime.datetime:
    """Calculate solar midnight time in the UTC timezone.

    Note that this claculates the solar midgnight that is closest
    to 00:00:00 of the specified date i.e. it may return a time that is on
    the previous day.

    :param observer: An observer viewing the sun at a specific, latitude, longitude and elevation
    :param date:     Date to calculate for.
    :return:         The UTC date and time at which midnight occurs.
    """
    if date is None:
        date = today(tzinfo)

    jd = julianday(date)
    newt = jday_to_jcentury(jd + 0.5 + -observer.longitude / 360.0)

    eqtime = eq_of_time(newt)
    timeUTC = (-observer.longitude * 4.0) - eqtime

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


def zenith(
    observer: Observer,
    dateandtime: datetime.datetime,
) -> float:
    """Calculate the zenith angle of the sun.

    :param dateandtime: The date and time for which to calculate the angle.
    :param observer:    Observer to calculate the solar zenith for
    :return:            The zenith angle in degrees.

    If `dateandtime` is a naive Python datetime then it is assumed to be
    in the UTC timezone.
    """

    if observer.latitude > 89.8:
        latitude = 89.8
    elif observer.latitude < -89.8:
        latitude = -89.8
    else:
        latitude = observer.latitude

    longitude = observer.longitude

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


def azimuth(
    observer: Observer,
    dateandtime: datetime.datetime,
) -> float:
    """Calculate the azimuth angle of the sun.

    :param dateandtime: The date and time for which to calculate the angle.
    :param observer:    Observer to calculate the solar azimuth for
    :return:            The azimuth angle in degrees clockwise from North.

    If `dateandtime` is a naive Python datetime then it is assumed to be
    in the UTC timezone.
    """

    if observer.latitude > 89.8:
        latitude = 89.8
    elif observer.latitude < -89.8:
        latitude = -89.8
    else:
        latitude = observer.latitude

    longitude = observer.longitude

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
    observer: Observer,
    dateandtime: Optional[datetime.datetime] = None,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> float:
    """Calculate the elevation angle of the sun.

    :param observer:    Observer to calculate the solar elevation for
    :param dateandtime: The date and time for which to calculate the angle.
    :return:            The elevation angle in degrees above the horizon.

    If `dateandtime` is a naive Python datetime then it is assumed to be
    in the UTC timezone.
    """

    if dateandtime is None:
        dateandtime = local.now(tzinfo)

    return 90 - zenith(observer, dateandtime)


def dawn(
    observer: Observer,
    date: Optional[datetime.date] = None,
    depression: float = 6.0,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> datetime.datetime:
    """Calculate dawn time in the UTC timezone.

    :param observer:   Observer to calculate dawn for
    :param date:       Date to calculate for.
    :param depression: Number of degrees below the horizon to use to calculate dawn
    :param tzinfo:     Timezone to return times in. Default is UTC.
    :return:           Date and time at which dawn occurs.
    """
    if date is None:
        date = today()

    try:
        return time_of_transit(
            observer, date, 90 + depression, SunDirection.RISING
        ).astimezone(tzinfo)
    except ValueError as exc:
        if exc.args[0] == "math domain error":
            raise AstralError(
                f"Sun never reaches {depression} degrees below the horizon, at this location."
            )
        else:
            raise


def sunrise(
    observer: Observer,
    date: Optional[datetime.date] = None,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> datetime.datetime:
    """Calculate sunrise time in the UTC timezone.

    :param observer: Observer to calculate sunrise for
    :param date:     Date to calculate for.
    :param tzinfo:   Timezone to return times in. Default is UTC.
    :return:         Date and time at which sunrise occurs.
    """
    if date is None:
        date = today()

    try:
        return time_of_transit(observer, date, 90 + 0.833, SunDirection.RISING).astimezone(tzinfo)
    except ValueError as exc:
        if exc.args[0] == "math domain error":
            z = zenith(observer, solar_noon(observer, date))
            if z > 90.0:
                msg = "Sun is always below the horizon on this day, at this location."
            else:
                msg = "Sun is always above the horizon on this day, at this location."
            raise AstralError(msg) from exc
        else:
            raise


def sunset(
    observer: Observer,
    date: Optional[datetime.date] = None,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> datetime.datetime:
    """Calculate sunset time in the UTC timezone.

    :param observer: Observer to calculate sunset for
    :param date:     Date to calculate for.
    :param tzinfo:   Timezone to return times in. Default is UTC.
    :return:         Date and time at which sunset occurs.
    """

    if date is None:
        date = today()

    try:
        return time_of_transit(observer, date, 90 + 0.833, SunDirection.SETTING).astimezone(tzinfo)
    except ValueError as exc:
        if exc.args[0] == "math domain error":
            z = zenith(observer, solar_noon(observer, date))
            if z > 90.0:
                msg = "Sun is always below the horizon on this day, at this location."
            else:
                msg = "Sun is always above the horizon on this day, at this location."
            raise AstralError(msg) from exc
        else:
            raise


def dusk(
    observer: Observer,
    date: Optional[datetime.date] = None,
    depression: float = 6.0,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> datetime.datetime:
    """Calculate dusk time in the UTC timezone.

    :param observer:   Observer to calculate dusk for
    :param date:       Date to calculate for.
    :param depression: Number of degrees below the horizon to use to calculate dusk
    :param tzinfo:     Timezone to return times in. Default is UTC.
    :return:           Date and time at which dusk occurs.
    """

    if date is None:
        date = today()

    try:
        return time_of_transit(observer, date, 90 + depression, SunDirection.SETTING).astimezone(tzinfo)
    except ValueError as exc:
        if exc.args[0] == "math domain error":
            raise AstralError(
                f"Sun never reaches {depression} degrees below the horizon, at this location."
            )
        else:
            raise


def daylight(
    observer: Observer,
    date: Optional[datetime.date] = None,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> Tuple[datetime.datetime, datetime.datetime]:
    """Calculate daylight start and end times in the UTC timezone.

    :param observer: Observer to calculate daylight for
    :param date:     Date to calculate for.
    :param tzinfo:   Timezone to return times in. Default is UTC.
    :return:         A tuple of the date and time at which daylight starts and ends.
    """
    if date is None:
        date = today()

    start = sunrise(observer, date, tzinfo)
    end = sunset(observer, date, tzinfo)

    return start, end


def night(
    observer: Observer,
    date: Optional[datetime.date] = None,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> Tuple[datetime.datetime, datetime.datetime]:
    """Calculate night start and end times in the UTC timezone.

    Night is calculated to be between astronomical dusk on the
    date specified and astronomical dawn of the next day.

    :param observer: Observer to calculate night for
    :param date:     Date to calculate for.
    :param tzinfo:   Timezone to return times in. Default is UTC.
    :return:         A tuple of the date and time at which night starts and ends.
    """
    if date is None:
        date = today()

    start = dusk(observer, date, 6, tzinfo)
    tomorrow = date + datetime.timedelta(days=1)
    end = dawn(observer, tomorrow, 6, tzinfo)

    return start, end


def time_at_altitude(
    observer: Observer,
    altitude: float,
    date: Optional[datetime.date] = None,
    direction: SunDirection = SunDirection.RISING,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> datetime.datetime:
    """Calculate the time in the UTC timezone when the sun is at
    the specified altitude on the specified date.

    Note: This method uses positive altitudes for those above the horizon.

    :param altitude:  Elevation in degrees above the horizon to calculate for.
    :param observer:  Observer to calculate for
    :param date:      Date to calculate for.
    :param direction: Determines whether the calculated time is for the sun rising or setting.
                      Use ``SunDirection.RISING`` or ``SunDirection.SETTING``. Default is rising.
    :param tzinfo:    Timezone to return times in. Default is UTC.
    :return:          Date and time at which the sun is at the required altitude.
    """

    if altitude > 90.0:
        altitude = 180.0 - altitude
        direction = SunDirection.SETTING

    if date is None:
        date = today()

    depression = 90 - altitude
    try:
        return time_of_transit(observer, date, depression, direction).astimezone(tzinfo)
    except ValueError as exc:
        if exc.args[0] == "math domain error":
            raise AstralError(
                f"Sun never reaches an altitude of {altitude} degrees"
                "at this location."
            )
        else:
            raise


def twilight(
    observer: Observer,
    date: Optional[datetime.date] = None,
    direction: SunDirection = SunDirection.RISING,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> Tuple[datetime.datetime, datetime.datetime]:
    """Returns the start and end times of Twilight in the UTC timezone when
    the sun is traversing in the specified direction.

    This method defines twilight as being between the time
    when the sun is at -6 degrees and sunrise/sunset.

    :param observer:  Observer to calculate twilight for
    :param date:      Date for which to calculate the times.
    :param direction: Determines whether the time is for the sun rising or setting.
                      Use ``astral.SunDirection.RISING`` or ``astral.SunDirection.SETTING``.
    :param tzinfo:    Timezone to return times in. Default is UTC.
    :return:          A tuple of the date and time at which twilight starts and ends.
    """

    if date is None:
        date = today()

    start = time_of_transit(observer, date, 90 + 6, direction).astimezone(tzinfo)
    if direction == SunDirection.RISING:
        end = sunrise(observer, date, tzinfo).astimezone(tzinfo)
    else:
        end = sunset(observer, date, tzinfo).astimezone(tzinfo)

    if direction == SunDirection.RISING:
        return start, end
    else:
        return end, start


def golden_hour(
    observer: Observer,
    date: Optional[datetime.date] = None,
    direction: SunDirection = SunDirection.RISING,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> Tuple[datetime.datetime, datetime.datetime]:
    """Returns the start and end times of the Golden Hour in the UTC timezone
    when the sun is traversing in the specified direction.

    This method uses the definition from PhotoPills i.e. the
    golden hour is when the sun is between 4 degrees below the horizon
    and 6 degrees above.

    :param date:      Date for which to calculate the times.
    :param observer:  Observer to calculate the golden hour for
    :param direction: Determines whether the time is for the sun rising or setting.
                      Use ``SunDirection.RISING`` or ``SunDirection.SETTING``.
    :param tzinfo:    Timezone to return times in. Default is UTC.
    :return:          A tuple of the date and time at which the Golden Hour starts and ends.
    """

    if date is None:
        date = today()

    start = time_of_transit(observer, date, 90 + 4, direction).astimezone(tzinfo)
    end = time_of_transit(observer, date, 90 - 6, direction).astimezone(tzinfo)

    if direction == SunDirection.RISING:
        return start, end
    else:
        return end, start


def blue_hour(
    observer: Observer,
    date: Optional[datetime.date] = None,
    direction: SunDirection = SunDirection.RISING,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> Tuple[datetime.datetime, datetime.datetime]:
    """Returns the start and end times of the Blue Hour in the UTC timezone
    when the sun is traversing in the specified direction.

    This method uses the definition from PhotoPills i.e. the
    blue hour is when the sun is between 6 and 4 degrees below the horizon.

    :param observer:  Observer to calculate the blue hour for
    :param date:      Date for which to calculate the times.
    :param direction: Determines whether the time is for the sun rising or setting.
                      Use ``SunDirection.RISING`` or ``SunDirection.SETTING``.
    :param tzinfo:    Timezone to return times in. Default is UTC.
    :return:          A tuple of the date and time at which the Blue Hour starts and ends.
    """

    if date is None:
        date = today()

    start = time_of_transit(observer, date, 90 + 6, direction).astimezone(tzinfo)
    end = time_of_transit(observer, date, 90 + 4, direction).astimezone(tzinfo)

    if direction == SunDirection.RISING:
        return start, end
    else:
        return end, start


def rahukaalam(
    observer: Observer,
    date: Optional[datetime.date] = None,
    daytime: bool = True,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> Tuple[datetime.datetime, datetime.datetime]:
    """Calculate ruhakaalam times in the UTC timezone.

    :param observer: Observer to calculate rahukaalam for
    :param date:     Date to calculate for.
    :param daytime:  If True calculate for the day time else calculate for the night time.
    :param tzinfo:   Timezone to return times in. Default is UTC.
    :return:         Tuple containing the start and end times for Rahukaalam.
    """

    if date is None:
        date = today()

    if daytime:
        start = sunrise(observer, date, tzinfo)
        end = sunset(observer, date, tzinfo)
    else:
        start = sunset(observer, date, tzinfo)
        oneday = datetime.timedelta(days=1)
        end = sunrise(observer, date + oneday, tzinfo)

    octant_duration = datetime.timedelta(seconds=(end - start).seconds / 8)

    # Mo,Sa,Fr,We,Th,Tu,Su
    octant_index = [1, 6, 4, 5, 3, 2, 7]

    weekday = date.weekday()
    octant = octant_index[weekday]

    start = start + (octant_duration * octant)
    end = start + octant_duration

    return start, end


def sun(
    observer: Observer,
    date: Optional[datetime.date] = None,
    dawn_dusk_depression: float = 6.0,
    tzinfo: datetime.tzinfo = pytz.utc,
) -> Dict:
    """Calculate all the info for the sun at once.

    :param observer:             Observer for which to calculate the times of the sun
    :param date:                 Date to calculate for.
    :param dawn_dusk_depression: Depression to use to calculate dawn and dusk
    :param tzinfo:               Timezone to return times in. Default is UTC.
    :returns:                    Dictionary with keys ``dawn``, ``sunrise``, ``noon``,
                                 ``sunset`` and ``dusk`` whose values are the results of
                                 the corresponding methods.
    """

    return {
        "dawn": dawn(observer, date, dawn_dusk_depression, tzinfo),
        "sunrise": sunrise(observer, date, tzinfo),
        "noon": solar_noon(observer, date, tzinfo),
        "sunset": sunset(observer, date, tzinfo),
        "dusk": dusk(observer, date, dawn_dusk_depression, tzinfo),
    }
