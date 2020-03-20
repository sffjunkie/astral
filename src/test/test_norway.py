from __future__ import unicode_literals

import pytest
import astral
from datetime import datetime, timedelta
import pytz
from astral import sun


def _next_event(obs: astral.Observer, dt: datetime, event: str):
    for offset in range(0, 365):
        newdate = dt + timedelta(days=offset)
        try:
            t = getattr(sun, event)(date=newdate, observer=obs)
            return t
        except ValueError:
            pass
    assert False, "Should be unreachable"  # pragma: no cover


def test_NorwaySunUp():
    """Test location in Norway where the sun doesn't set in summer."""
    june = datetime(2019, 6, 5, tzinfo=pytz.utc)
    obs = astral.Observer(69.6, 18.8, 0.0)

    with pytest.raises(ValueError):
        sun.sunrise(obs, june)
    with pytest.raises(ValueError):
        sun.sunset(obs, june)

    # Find the next sunset and sunrise:
    next_sunrise = _next_event(obs, june, "sunrise")
    next_sunset = _next_event(obs, june, "sunset")

    assert next_sunset < next_sunrise
