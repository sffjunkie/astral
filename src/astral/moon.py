"""Moon phase, rise and set times

Right ascension, declination and distance of moon calcaulation
from

LOW-PRECISION FORMULAE FOR PLANETARY POSITIONS
http://articles.adsabs.harvard.edu/pdf/1979ApJS...41..391V
"""

import datetime
from dataclasses import dataclass, field, replace
from math import asin, atan2, cos, degrees, fabs, pi, radians, sin, sqrt
from typing import Callable, List, Optional, Union

try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo  # type: ignore

from astral import AstralBodyPosition, Observer, now, today
from astral.julian import julianday, julianday_2000
from astral.sidereal import lmst
from astral.table4 import Table4Row, table4_u, table4_v, table4_w

__all__ = ["moonrise", "moonset", "phase"]

# Using 1896 arc seconds as moon's apparent diameter
MOON_APPARENT_RADIUS = 1896.0 / (60.0 * 60.0)

Degrees = float
Radians = float
Revolutions = float
ArgumentFunc = Optional[Callable[[float], float]]


@dataclass
class NoTransit:
    parallax: float = field(default_factory=float)


@dataclass
class TransitEvent:
    event: str
    when: datetime.time = field(default_factory=datetime.time)
    azimuth: float = field(default_factory=float)
    distance: float = field(default_factory=float)


def interpolate(f0: float, f1: float, f2: float, p: float) -> float:
    """3-point interpolation"""
    a = f1 - f0
    b = f2 - f1 - a
    f = f0 + p * (2 * a + b * (2 * p - 1))
    return f


def sgn(value1: Union[float, datetime.timedelta]) -> int:
    """Test whether value1 and value2 have the same sign"""
    if isinstance(value1, datetime.timedelta):
        value1 = value1.total_seconds()

    if value1 < 0:
        return -1
    elif value1 > 0:
        return 1
    else:
        return 0


def moon_mean_longitude(jd2000: float) -> Revolutions:
    _mean_longitude = 0.606434 + 0.03660110129 * jd2000
    _mean_longitude = _mean_longitude - int(_mean_longitude)
    return _mean_longitude


def moon_mean_anomoly(jd2000: float) -> Revolutions:
    _mean_anomoly = 0.374897 + 0.03629164709 * jd2000
    _mean_anomoly = _mean_anomoly - int(_mean_anomoly)
    return _mean_anomoly


def moon_argument_of_latitude(jd2000: float) -> Revolutions:
    _argument_of_latitude = 0.259091 + 0.03674819520 * jd2000
    _argument_of_latitude = _argument_of_latitude - int(_argument_of_latitude)
    return _argument_of_latitude


def moon_mean_elongation_from_sun(jd2000: float) -> Revolutions:
    _mean_elongation_from_sun = 0.827362 + 0.03386319198 * jd2000
    _mean_elongation_from_sun = _mean_elongation_from_sun - int(
        _mean_elongation_from_sun
    )
    return _mean_elongation_from_sun


def longitude_lunar_ascending_node(jd2000: float) -> Revolutions:
    _longitude_lunar_ascending_node = moon_mean_longitude(
        jd2000
    ) - moon_argument_of_latitude(jd2000)
    return _longitude_lunar_ascending_node


def sun_mean_longitude(jd2000: float) -> Revolutions:
    _sun_mean_longitude = 0.779072 + 0.00273790931 * jd2000
    _sun_mean_longitude = _sun_mean_longitude - int(_sun_mean_longitude)
    return _sun_mean_longitude


def sun_mean_anomoly(jd2000: float) -> Revolutions:
    _sun_mean_anomoly = 0.993126 + 0.00273777850 * jd2000
    _sun_mean_anomoly = _sun_mean_anomoly - int(_sun_mean_anomoly)
    return _sun_mean_anomoly


def venus_mean_longitude(jd2000: float) -> Revolutions:
    _venus_mean_longitude = 0.505498 + 0.00445046867 * jd2000
    _venus_mean_longitude = _venus_mean_longitude - int(_venus_mean_longitude)
    return _venus_mean_longitude


def moon_position(jd2000: float) -> AstralBodyPosition:
    """Calculate right ascension, declination and geocentric distance for the moon"""

    argument_values: List[Union[float, None]] = [
        moon_mean_longitude(jd2000),  # 1 = Lm
        moon_mean_anomoly(jd2000),  # 2 = Gm
        moon_argument_of_latitude(jd2000),  # 3 = Fm
        moon_mean_elongation_from_sun(jd2000),  # 4 = D
        longitude_lunar_ascending_node(jd2000),  # 5 = Om
        None,  # 6
        sun_mean_longitude(jd2000),  # 7 = Ls
        sun_mean_anomoly(jd2000),  # 8 = Gs
        None,  # 9
        None,  # 10
        None,  # 11
        venus_mean_longitude(jd2000),  # 12 = L2
    ]

    T = jd2000 / 36525 + 1

    def _calc_value(table: List[Table4Row]) -> float:
        result = 0.0
        for row in table:
            revolutions: float = 0.0
            for arg_number, multiplier in row.argument_multiplers.items():
                if multiplier != 0:
                    arg_value = argument_values[arg_number - 1]
                    if arg_value:
                        value = arg_value * multiplier
                        revolutions += value
                    else:
                        raise ValueError

            t_multipler = T if row.t else 1
            result += row.coefficient * t_multipler * row.sincos(revolutions * 2 * pi)

        return result

    v = _calc_value(table4_v)
    u = _calc_value(table4_u)
    w = _calc_value(table4_w)

    s = w / sqrt(u - v * v)
    right_ascension = asin(s) + (argument_values[0] or 0) * 2 * pi  # In radians

    s = v / sqrt(u)
    declination = asin(s)  # In radians

    distance = 60.40974 * sqrt(u)  # In Earth radii (≈6378km)

    return AstralBodyPosition(right_ascension, declination, distance)


def moon_transit_event(
    hour: float,
    lmst: Degrees,
    latitude: Degrees,
    distance: float,
    window: List[AstralBodyPosition],
) -> Union[TransitEvent, NoTransit]:
    """Check if the moon transits the horizon within the window.

    Args:
        hour: Hour of the day
        lmst: Local mean sidereal time in degrees
        latitude: Observer latitude
        distance: Distance to the moon
        window: Sliding window of moon positions that covers a part of the day
    """
    mst = radians(lmst)
    hour_angle = [0.0, 0.0, 0.0]

    k1 = radians(15 * 1.0027379097096138907193594760917)

    if window[2].right_ascension < window[0].right_ascension:
        window[2].right_ascension = window[2].right_ascension + 2 * pi

    hour_angle[0] = mst - window[0].right_ascension + (hour * k1)
    hour_angle[2] = mst - window[2].right_ascension + (hour * k1) + k1
    hour_angle[1] = (hour_angle[2] + hour_angle[0]) / 2

    window[1].declination = (window[2].declination + window[0].declination) / 2

    sl = sin(radians(latitude))
    cl = cos(radians(latitude))

    # moon apparent radius + parallax correction
    z = cos(radians(90 + MOON_APPARENT_RADIUS - (41.685 / distance)))

    if hour == 0:
        window[0].distance = (
            sl * sin(window[0].declination)
            + cl * cos(window[0].declination) * cos(hour_angle[0])
            - z
        )

    window[2].distance = (
        sl * sin(window[2].declination)
        + cl * cos(window[2].declination) * cos(hour_angle[2])
        - z
    )

    if sgn(window[0].distance) == sgn(window[2].distance):
        return NoTransit(window[2].distance)

    window[1].distance = (
        sl * sin(window[1].declination)
        + cl * cos(window[1].declination) * cos(hour_angle[1])
        - z
    )

    a = 2 * window[2].distance - 4 * window[1].distance + 2 * window[0].distance
    b = 4 * window[1].distance - 3 * window[0].distance - window[2].distance
    discriminant = b * b - 4 * a * window[0].distance

    if discriminant < 0:
        return NoTransit(window[2].distance)

    discriminant = sqrt(discriminant)
    e = (-b + discriminant) / (2 * a)
    if e > 1 or e < 0:
        e = (-b - discriminant) / (2 * a)

    time = hour + e + 1 / 120

    h = int(time)
    m = int((time - h) * 60)

    sd = sin(window[1].declination)
    cd = cos(window[1].declination)

    hour_angle_crossing = hour_angle[0] + e * (hour_angle[2] - hour_angle[0])
    sh = sin(hour_angle_crossing)
    ch = cos(hour_angle_crossing)

    x = cl * sd - sl * cd * ch
    y = -cd * sh

    az = degrees(atan2(y, x))
    if az < 0:
        az += 360
    if az > 360:
        az -= 360

    event_time = datetime.time(h, m, 0)
    if window[0].distance < 0 and window[2].distance > 0:
        return TransitEvent("rise", event_time, az, window[2].distance)

    if window[0].distance > 0 and window[2].distance < 0:
        return TransitEvent("set", event_time, az, window[2].distance)

    return NoTransit(window[2].distance)


def riseset(
    on: datetime.date,
    observer: Observer,
):
    """Calculate rise and set times"""
    jd2000 = julianday_2000(on)
    t0 = lmst(
        on,
        observer.longitude,
    )

    m: List[AstralBodyPosition] = []
    for interval in range(3):
        pos = moon_position(jd2000 + (interval * 0.5))
        m.append(pos)

    for interval in range(1, 3):
        if m[interval].right_ascension <= m[interval - 1].right_ascension:
            m[interval].right_ascension = m[interval].right_ascension + 2 * pi

    moon_position_window: List[AstralBodyPosition] = [
        replace(m[0]),  # copy m[0]
        AstralBodyPosition(),
        AstralBodyPosition(),
    ]

    rise_time = None
    set_time = None

    # events = []
    for hour in range(24):
        ph = (hour + 1) / 24
        moon_position_window[2].right_ascension = interpolate(
            m[0].right_ascension,
            m[1].right_ascension,
            m[2].right_ascension,
            ph,
        )
        moon_position_window[2].declination = interpolate(
            m[0].declination,
            m[1].declination,
            m[2].declination,
            ph,
        )

        transit_info = moon_transit_event(
            hour, t0, observer.latitude, m[1].distance, moon_position_window
        )
        if isinstance(transit_info, NoTransit):
            moon_position_window[2].distance = transit_info.parallax
        else:
            query_time = datetime.datetime(
                on.year, on.month, on.day, hour, 0, 0, tzinfo=datetime.timezone.utc
            )

            if transit_info.event == "rise":
                event_time = transit_info.when
                event = datetime.datetime(
                    on.year,
                    on.month,
                    on.day,
                    event_time.hour,
                    event_time.minute,
                    0,
                    tzinfo=datetime.timezone.utc,
                )
                if rise_time is None:
                    rise_time = event
                else:
                    rq_diff = (rise_time - query_time).total_seconds()
                    eq_diff = (event - query_time).total_seconds()
                    if set_time is not None:
                        sq_diff = (set_time - query_time).total_seconds()
                    else:
                        sq_diff = 0

                    update_rise_time = sgn(rq_diff) == sgn(eq_diff) and fabs(
                        rq_diff
                    ) > fabs(eq_diff)
                    update_rise_time |= sgn(rq_diff) != sgn(eq_diff) and (
                        set_time is not None and sgn(rq_diff) == sgn(sq_diff)
                    )

                    if update_rise_time:
                        rise_time = event
            elif transit_info.event == "set":
                event_time = transit_info.when
                event = datetime.datetime(
                    on.year,
                    on.month,
                    on.day,
                    event_time.hour,
                    event_time.minute,
                    0,
                    tzinfo=datetime.timezone.utc,
                )
                if set_time is None:
                    set_time = event
                else:
                    sq_diff = (set_time - query_time).total_seconds()
                    eq_diff = (event - query_time).total_seconds()
                    if rise_time is not None:
                        rq_diff = (rise_time - query_time).total_seconds()
                    else:
                        rq_diff = 0

                    update_set_time = sgn(sq_diff) == sgn(eq_diff) and fabs(
                        sq_diff
                    ) > fabs(eq_diff)
                    update_set_time |= sgn(sq_diff) != sgn(eq_diff) and (
                        rise_time is not None and sgn(rq_diff) == sgn(sq_diff)
                    )

                    if update_set_time:
                        set_time = event

        moon_position_window[0].right_ascension = moon_position_window[
            2
        ].right_ascension
        moon_position_window[0].declination = moon_position_window[2].declination
        moon_position_window[0].distance = moon_position_window[2].distance

    return rise_time, set_time


def moonrise(
    observer: Observer,
    date: Optional[datetime.date] = None,
    tzinfo: Union[str, datetime.tzinfo] = datetime.timezone.utc,
) -> Optional[datetime.datetime]:
    """Calculate the moon rise time

    Args:
        observer: Observer to calculate moonrise for
        date:     Date to calculate for. Default is today's date in the
                  timezone `tzinfo`.
        tzinfo:   Timezone to return times in. Default is UTC.

    Returns:
        Date and time at which moonrise occurs.
    """
    if isinstance(tzinfo, str):
        tzinfo = zoneinfo.ZoneInfo(tzinfo)  # type: ignore

    if date is None:
        date = today(tzinfo)  # type: ignore
    elif isinstance(date, datetime.datetime):
        date = date.date()

    info = riseset(date, observer)
    if info[0]:
        rise = info[0].astimezone(tzinfo)  # type: ignore
        rd = rise.date()
        if rd != date:
            if rd > date:
                delta = datetime.timedelta(days=-1)
            else:
                delta = datetime.timedelta(days=1)
            new_date = date + delta
            info = riseset(new_date, observer)
            if info[0]:
                rise = info[0].astimezone(tzinfo)  # type: ignore
                rd = rise.date()
                if rd != date:
                    rise = None
        return rise
    else:
        raise ValueError("Moon never rises on this date, at this location")


def moonset(
    observer: Observer,
    date: Optional[datetime.date] = None,
    tzinfo: Union[str, datetime.tzinfo] = datetime.timezone.utc,
) -> Optional[datetime.datetime]:
    """Calculate the moon set time

    Args:
        observer: Observer to calculate moonset for
        date:     Date to calculate for. Default is today's date in the
                  timezone `tzinfo`.
        tzinfo:   Timezone to return times in. Default is UTC.

    Returns:
        Date and time at which moonset occurs.
    """
    if isinstance(tzinfo, str):
        tzinfo = zoneinfo.ZoneInfo(tzinfo)  # type: ignore

    if date is None:
        date = today(tzinfo)  # type: ignore
    elif isinstance(date, datetime.datetime):
        date = date.date()

    info = riseset(date, observer)
    if info[1]:
        set = info[1].astimezone(tzinfo)  # type: ignore
        sd = set.date()
        if sd != date:
            if sd > date:
                delta = datetime.timedelta(days=-1)
            else:
                delta = datetime.timedelta(days=1)
            new_date = date + delta
            info = riseset(new_date, observer)
            if info[1]:
                set = info[1].astimezone(tzinfo)  # type: ignore
                sd = set.date()
                if sd != date:
                    set = None
        return set
    else:
        raise ValueError("Moon never sets on this date, at this location")


def azimuth(
    observer: Observer,
    at: Optional[datetime.datetime] = None,
) -> Degrees:
    if at is None:
        at = now()

    jd2000 = julianday_2000(at)
    position = moon_position(jd2000)
    lst0: Radians = radians(lmst(at, observer.longitude))
    hourangle: Radians = lst0 - position.right_ascension

    sh = sin(hourangle)
    ch = cos(hourangle)
    sd = sin(position.declination)
    cd = cos(position.declination)
    sl = sin(radians(observer.latitude))
    cl = cos(radians(observer.latitude))

    x = -ch * cd * sl + sd * cl
    y = -sh * cd
    azimuth = degrees(atan2(y, x)) % 360
    return azimuth


def elevation(
    observer: Observer,
    at: Optional[datetime.datetime] = None,
):
    if at is None:
        at = now()

    jd2000 = julianday_2000(at)
    position = moon_position(jd2000)
    lst0: Radians = radians(lmst(at, observer.longitude))
    hourangle: Radians = lst0 - position.right_ascension

    sh = sin(hourangle)
    ch = cos(hourangle)
    sd = sin(position.declination)
    cd = cos(position.declination)
    sl = sin(radians(observer.latitude))
    cl = cos(radians(observer.latitude))

    x = -ch * cd * sl + sd * cl
    y = -sh * cd

    z = ch * cd * cl + sd * sl
    r = sqrt(x * x + y * y)
    elevation = degrees(atan2(z, r))

    return elevation


def zenith(
    observer: Observer,
    at: Optional[datetime.datetime] = None,
):
    return 90 - elevation(observer, at)


def _phase_asfloat(date: datetime.date) -> float:
    jd = julianday(date)
    dt = pow((jd - 2382148), 2) / (41048480 * 86400)
    t = (jd + dt - 2451545.0) / 36525
    t2 = pow(t, 2)
    t3 = pow(t, 3)

    d = 297.85 + (445267.1115 * t) - (0.0016300 * t2) + (t3 / 545868)
    d = radians(d % 360.0)

    m = 357.53 + (35999.0503 * t)
    m = radians(m % 360.0)

    m1 = 134.96 + (477198.8676 * t) + (0.0089970 * t2) + (t3 / 69699)
    m1 = radians(m1 % 360.0)

    elong = degrees(d) + 6.29 * sin(m1)
    elong -= 2.10 * sin(m)
    elong += 1.27 * sin(2 * d - m1)
    elong += 0.66 * sin(2 * d)
    elong = elong % 360.0
    elong = int(elong)
    moon = ((elong + 6.43) / 360) * 28
    return moon


def phase(date: Optional[datetime.date] = None) -> float:
    """Calculates the phase of the moon on the specified date.

    Args:
        date: The date to calculate the phase for. Dates are always in the UTC timezone.
              If not specified then today's date is used.

    Returns:
        A number designating the phase.

        ============  ==============
        0 .. 6.99     New moon
        7 .. 13.99    First quarter
        14 .. 20.99   Full moon
        21 .. 27.99   Last quarter
        ============  ==============
    """

    if date is None:
        date = today()

    moon = _phase_asfloat(date)
    if moon >= 28.0:
        moon -= 28.0
    return moon
