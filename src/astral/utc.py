"""Sun calculations in the UTC timezone"""

import datetime
from typing import Dict, Tuple, Optional

import pytz

import astral.calc
from astral import AstralError, Observer, SunDirection


def now() -> datetime.datetime:
    return pytz.utc.localize(datetime.datetime.utcnow())


def today() -> datetime.date:
    return now().date()


def solar_noon(
    observer: Observer, date: Optional[datetime.date] = None
) -> datetime.datetime:
    """Calculate solar noon time in the UTC timezone.

    :param observer: Observer to calculate noon time for
    :param date:     Date to calculate for.
    :return:         The UTC date and time at which noon occurs.
    """
    if date is None:
        date = today()

    return astral.calc.solar_noon(observer.longitude, date)


def solar_midnight(
    observer: Observer, date: Optional[datetime.date] = None
) -> datetime.datetime:
    """Calculate solar midnight time in the UTC timezone.

    Note that this claculates the solar midgnight that is closest
    to 00:00:00 of the specified date i.e. it may return a time that is on
    the previous daytime.

    :param observer: Observer to calculate solar midnight for
    :param date:     Date to calculate for.
    :return:         The UTC date and time at which midnight occurs.
    """
    if date is None:
        date = today()

    return astral.calc.solar_midnight(observer.longitude, date)


def azimuth(
    observer: Observer, dateandtime: Optional[datetime.datetime] = None
) -> float:
    """Calculate the azimuth angle of the sun.

    :param observer:    The Observer to calculate the solar azimuth for
    :param dateandtime: The date and time for which to calculate the angle.
    :return:            The azimuth angle in degrees clockwise from North.

    If `dateandtime` is a naive Python datetime then it is assumed to be
    in the UTC timezone.
    """

    if dateandtime is None:
        dateandtime = now()

    return astral.calc.azimuth(dateandtime, observer.latitude, observer.longitude)


def zenith(
    observer: Observer, dateandtime: Optional[datetime.datetime] = None
) -> float:
    """Calculates the solar zenith angle.

    :param observer:    The Observer to calculate the solar zenith for
    :param dateandtime: The date and time for which to calculate the angle.
    :return:            The zenith angle in degrees from vertical.

    If `dateandtime` is a naive Python datetime then it is assumed to be
    in the UTC timezone.
    """

    if dateandtime is None:
        dateandtime = now()

    return astral.calc.zenith(dateandtime, observer.latitude, observer.longitude)


def altitude(
    observer: Observer, dateandtime: Optional[datetime.datetime] = None
) -> float:
    """Calculate the elevation angle of the sun.

    :param observer:    The Observer to calculate the solar elevation for
    :param dateandtime: The date and time for which to calculate the angle.
    :return:            The elevation angle in degrees above the horizon.

    If `dateandtime` is a naive Python datetime then it is assumed to be
    in the UTC timezone.
    """

    if dateandtime is None:
        dateandtime = now()

    return astral.calc.altitude(dateandtime, observer.latitude, observer.longitude)


def dawn(
    observer: Observer, date: Optional[datetime.date] = None, depression: float = 6.0
) -> datetime.datetime:
    """Calculate dawn time in the UTC timezone.

    :param observer:   The Observer to calculate dawn for
    :param date:       Date to calculate for.
    :param depression: The number of degrees below the horizon to use to calculate dawn
    :return:           The UTC date and time at which dawn occurs.
    """
    if date is None:
        date = today()

    try:
        return astral.calc.time_of_transit(
            observer.latitude,
            observer.longitude,
            observer.elevation,
            date,
            90 + depression,
            SunDirection.RISING,
        )
    except ValueError as exc:
        if exc.args[0] == "math domain error":
            raise AstralError(
                f"Sun never reaches {depression} degrees below the horizon, at this location."
            )
        else:
            raise


def sunrise(
    observer: Observer, date: Optional[datetime.date] = None
) -> datetime.datetime:
    """Calculate sunrise time in the UTC timezone.

    :param observer: The Observer to calculate sunrise for
    :param date:     Date to calculate for.
    :return:         The UTC date and time at which sunrise occurs.
    """
    if date is None:
        date = today()

    try:
        return astral.calc.time_of_transit(
            observer.latitude,
            observer.longitude,
            observer.elevation,
            date,
            90 + 0.833,
            SunDirection.RISING,
        )
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
    observer: Observer, date: Optional[datetime.date] = None
) -> datetime.datetime:
    """Calculate sunset time in the UTC timezone.

    :param observer: Observer to calculate sunset for
    :param date:     Date to calculate for.
    :return:         The UTC date and time at which sunset occurs.
    """

    if date is None:
        date = today()

    try:
        return astral.calc.time_of_transit(
            observer.latitude,
            observer.longitude,
            observer.elevation,
            date,
            90 + 0.833,
            SunDirection.SETTING,
        )
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
    observer: Observer, date: Optional[datetime.date] = None, depression: float = 6.0
) -> datetime.datetime:
    """Calculate dusk time in the UTC timezone.

    :param observer:   Observer to calculate dusk for
    :param date:       Date to calculate for.
    :param depression: The number of degrees below the horizon to use to calculate dusk
    :return:           The UTC date and time at which dusk occurs.
    """

    if date is None:
        date = today()

    try:
        return astral.calc.time_of_transit(
            observer.latitude,
            observer.longitude,
            observer.elevation,
            date,
            90 + depression,
            SunDirection.SETTING,
        )
    except ValueError as exc:
        if exc.args[0] == "math domain error":
            raise AstralError(
                f"Sun never reaches {depression} degrees below the horizon, at this location."
            )
        else:
            raise


def daylight(
    observer: Observer, date: Optional[datetime.date] = None
) -> Tuple[datetime.datetime, datetime.datetime]:
    """Calculate daylight start and end times in the UTC timezone.

    :param observer: Observer to calculate daylight for
    :param date:     Date to calculate for.
    :return:         A tuple of the UTC date and time at which daylight starts and ends.
    """
    if date is None:
        date = today()

    start = sunrise(observer, date)
    end = sunset(observer, date)

    return start, end


def night(
    observer: Observer, date: Optional[datetime.date] = None
) -> Tuple[datetime.datetime, datetime.datetime]:
    """Calculate night start and end times in the UTC timezone.

    Night is calculated to be between astronomical dusk on the
    date specified and astronomical dawn of the next day.

    :param observer: Observer to calculate night for
    :param date:     Date to calculate for.
    :return:         A tuple of the UTC date and time at which night starts and ends.
    """
    if date is None:
        date = today()

    start = dusk(observer, date, 6)
    tomorrow = date + datetime.timedelta(days=1)
    end = dawn(observer, tomorrow, 6)

    return start, end


def time_at_altitude(
    observer: Observer,
    altitude: float,
    date: Optional[datetime.date] = None,
    direction: SunDirection = SunDirection.RISING,
) -> datetime.datetime:
    """Calculate the time in the UTC timezone when the sun is at
    the specified altitude on the specified date.

    Note: This method uses positive altitudes for those above the horizon.

    :param altitude: Elevation in degrees above the horizon to calculate for.
    :param observer:  Observer to calculate for
    :param date:      Date to calculate for.
    :param direction: Determines whether the calculated time is for the sun rising or setting.
                      Use ``SunDirection.RISING`` or ``SunDirection.SETTING``. Default is rising.

    :return: The UTC date and time at which the sun is at the required altitude.
    """

    if altitude > 90.0:
        altitude = 180.0 - altitude
        direction = SunDirection.SETTING

    if date is None:
        date = today()

    depression = 90 - altitude
    try:
        return astral.calc.time_of_transit(
            observer.latitude,
            observer.longitude,
            observer.elevation,
            date,
            depression,
            direction,
        )
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
) -> Tuple[datetime.datetime, datetime.datetime]:
    """Returns the start and end times of Twilight in the UTC timezone when
    the sun is traversing in the specified direction.

    This method defines twilight as being between the time
    when the sun is at -6 degrees and sunrise/sunset.

    :param observer:  The Observer to calculate twilight for
    :param date:      The date for which to calculate the times.
    :param direction: Determines whether the time is for the sun rising or setting.
                      Use ``astral.SunDirection.RISING`` or ``astral.SunDirection.SETTING``.
    :return:          A tuple of the UTC date and time at which twilight starts and ends.
    """

    if date is None:
        date = today()

    start = time_at_altitude(observer, -6, date, direction)
    if direction == SunDirection.RISING:
        end = sunrise(observer, date)
    else:
        end = sunset(observer, date)

    if direction == SunDirection.RISING:
        return start, end
    else:
        return end, start


def golden_hour(
    observer: Observer,
    date: Optional[datetime.date] = None,
    direction: SunDirection = SunDirection.RISING,
) -> Tuple[datetime.datetime, datetime.datetime]:
    """Returns the start and end times of the Golden Hour in the UTC timezone
    when the sun is traversing in the specified direction.

    This method uses the definition from PhotoPills i.e. the
    golden hour is when the sun is between 4 degrees below the horizon
    and 6 degrees above.

    :param date:      The date for which to calculate the times.
    :param observer:  The Observer to calculate the golden hour for
    :param direction: Determines whether the time is for the sun rising or setting.
                      Use ``SunDirection.RISING`` or ``SunDirection.SETTING``.
    :return:          A tuple of the UTC date and time at which the Golden Hour starts and ends.
    """

    if date is None:
        date = today()

    start = time_at_altitude(observer, -4, date, direction)
    end = time_at_altitude(observer, 6, date, direction)

    if direction == SunDirection.RISING:
        return start, end
    else:
        return end, start


def blue_hour(
    observer: Observer,
    date: Optional[datetime.date] = None,
    direction: SunDirection = SunDirection.RISING,
) -> Tuple[datetime.datetime, datetime.datetime]:
    """Returns the start and end times of the Blue Hour in the UTC timezone
    when the sun is traversing in the specified direction.

    This method uses the definition from PhotoPills i.e. the
    blue hour is when the sun is between 6 and 4 degrees below the horizon.

    :param observer:  The Observer to calculate the blue hour for
    :param date:      The date for which to calculate the times.
    :param direction: Determines whether the time is for the sun rising or setting.
                      Use ``SunDirection.RISING`` or ``SunDirection.SETTING``.
    :return:          A tuple of the UTC date and time at which the Blue Hour starts and ends.
    """

    if date is None:
        date = today()

    start = time_at_altitude(observer, -6, date, direction)
    end = time_at_altitude(observer, -4, date, direction)

    if direction == SunDirection.RISING:
        return start, end
    else:
        return end, start


def rahukaalam(
    observer: Observer, date: Optional[datetime.date] = None, daytime: bool = True
) -> Tuple[datetime.datetime, datetime.datetime]:
    """Calculate ruhakaalam times in the UTC timezone.

    :param observer: The Observer to calculate rahukaalam for
    :param date:     Date to calculate for.
    :param daytime:  If True calculate for the day time else calculate for the night time.
    :return:         Tuple containing the start and end times for Rahukaalam.
    """

    if date is None:
        date = today()

    if daytime:
        start = sunrise(observer, date)
        end = sunset(observer, date)
    else:
        start = sunset(observer, date)
        oneday = datetime.timedelta(days=1)
        end = sunrise(observer, date + oneday)

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
) -> Dict:
    """Calculate all the info for the sun at once.
    All times are returned in the UTC timezone.

    :param observer:             The Observer for which to calculate the times of the sun
    :param date:                 Date to calculate for.
    :param dawn_dusk_depression: The depression to use to calculate dawn and dusk
    :returns:                    Dictionary with keys ``dawn``, ``sunrise``, ``noon``,
                                 ``sunset`` and ``dusk`` whose values are the results of
                                 the corresponding methods.
    """

    return {
        "dawn": dawn(observer, date, dawn_dusk_depression),
        "sunrise": sunrise(observer, date),
        "noon": solar_noon(observer, date),
        "sunset": sunset(observer, date),
        "dusk": dusk(observer, date, dawn_dusk_depression),
    }
