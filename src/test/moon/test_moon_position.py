from datetime import date

from astral.moon import julianday, moon_position


def test_moon_position():
    d = date(1969, 6, 28)
    jd = julianday(d)
    jd2000 = jd - 2451545  # Julian day relative to Jan 1.5, 2000
    _pos1 = moon_position(jd2000)

    d = date(1992, 4, 12)
    jd = julianday(d)
    jd2000 = jd - 2451545  # Julian day relative to Jan 1.5, 2000
    _pos2 = moon_position(jd2000)
    pass


if __name__ == "__main__":
    test_moon_position()
