# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import pytest
import astral
from datetime import datetime, timedelta, tzinfo
from pytz import UTC


def _next_event(location, datetime, event):
    for offset in range(0, 365):
        try:
            return getattr(location, event)(date=datetime+timedelta(days=offset))
        except astral.AstralError:
            pass
    assert False, "Should be unreachable"
        

def test_Midnight_Sun():
    """Test location in Norway where the sun doesn't set in summer."""
    june = datetime(2019, 6, 5, tzinfo=UTC)
    location = astral.Location(("Tisnes", "Norway", 69.6, 18.8, "UTC"))

    # This is expected
    with pytest.raises(astral.AstralError):
        location.sunrise(date=june, local=False)
    with pytest.raises(astral.AstralError):
        location.sunset(date=june, local=False)
    
    # Find the next sunset and sunrise:
    next_sunrise = _next_event(location, june, 'sunrise')
    next_sunset = _next_event(location, june, 'sunset')
    
    # This should be true, but it's not.
    assert next_sunset < next_sunrise
        

def test_elevations():
    june = datetime(2019, 6, 5, tzinfo=UTC)
    # location = astral.Location(("Perth", "Australia", -31.8584265, 115.769342, "UTC"))
    location = astral.Location(("Tisnes", "Norway", 69.6, 18.8, "UTC"))

    failed = []
    for j in [astral.SUN_RISING, astral.SUN_SETTING]:
        for i in range(-90,90):
            try:
                time = location.time_at_elevation(i, direction=j, date=june, local=False)
            except astral.AstralError:
                continue
            elevation = location.solar_elevation(time)
            # Sunrise not at right time.
            delta = abs(elevation - i)
            if delta > 0.05:
                failed.append((time.isoformat()[:19], j, i, elevation))
                min_time = time
                min_delta = delta
                for d in range(-360,360):
                    t = time+timedelta(seconds=d)
                    e = location.solar_elevation(t)
                    d = abs(e - i)
                    if d < min_delta:
                        min_delta = d
                        min_time = t
                failed.append(("Closest", min_time.isoformat()[:19], min_delta))

    # This fails.    
    assert failed == []


def test_elevation_altitude():
    june = datetime(2019, 6, 5, 2, 0, 0, tzinfo=UTC)
    location = astral.Location(("Perth", "Australia", -31.8584265, 115.769342, "UTC"))

    e_ground = location.solar_elevation(june)

    location.elevation = 1000
    e_altitude = location.solar_elevation(june)

    # This should fail, since when at altitude the elevation should be less
    assert e_ground > e_altitude
