from datetime import datetime, timedelta, timezone

import pytest

import astral
from astral import sun
from astral.location import Location


def _next_event(obs: astral.Observer, dt: datetime, event: str):
    for offset in range(0, 365):
        newdate = dt + timedelta(days=offset)
        try:
            t = getattr(sun, event)(date=newdate, observer=obs)
            return t
        except ValueError:
            pass
    assert False, "Should be unreachable"  # pragma: no cover


def test_NorwaySunUp(tromso: Location):
    """Test location in Norway where the sun doesn't set in summer."""
    june = datetime(2019, 6, 5, tzinfo=timezone.utc)

    with pytest.raises(ValueError):
        sun.sunrise(tromso.observer, june)
    with pytest.raises(ValueError):
        sun.sunset(tromso.observer, june)

    # Find the next sunset and sunrise:
    next_sunrise = _next_event(tromso.observer, june, "sunrise")
    next_sunset = _next_event(tromso.observer, june, "sunset")

    assert next_sunset < next_sunrise
