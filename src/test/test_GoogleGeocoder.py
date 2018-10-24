import io
import os.path
import pytest

from astral import GoogleGeocoder

def read_contents(*names, **kwargs):
    return io.open(
        os.path.join(*names),
        encoding=kwargs.get("encoding", "utf8")
    ).read()

try:
    api_key = read_contents(os.path.dirname(__file__), '.api_key').strip()
except IOError as exc:
    raise ValueError("Google now requires an API key to be provided") from exc

@pytest.mark.webtest
def test_GoogleLocator_WithAPIKey():
    locator = GoogleGeocoder(api_key=api_key)
    l = locator['Eiffel Tower']
    assert l is not None
