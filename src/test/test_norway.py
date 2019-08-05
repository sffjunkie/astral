from __future__ import unicode_literals

import pytest
import astral
from datetime import datetime, timedelta
import pytz
from astral import sun


def _next_event(location, datetime, event):
    for offset in range(0, 365):
        newdate = datetime + timedelta(days=offset)
        try:
            t = getattr(sun, event)(date=newdate, observer=location)
            return t
        except Exception:
            pass
    assert False, "Should be unreachable"


def test_NorwaySunUp():
    """Test location in Norway where the sun doesn't set in summer."""
    june = datetime(2019, 6, 5, tzinfo=pytz.utc)
    location = astral.LocationInfo("Tisnes", "Norway", "UTC", 69.6, 18.8)

    with pytest.raises(astral.AstralError):
        sun.sunrise(location, june)
    with pytest.raises(astral.AstralError):
        sun.sunset(location, june)

    # Find the next sunset and sunrise:
    next_sunrise = _next_event(location, june, "sunrise")
    next_sunset = _next_event(location, june, "sunset")

    assert next_sunset < next_sunrise
