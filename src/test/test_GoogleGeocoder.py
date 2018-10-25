import io
import os
import pytest

from astral import GoogleGeocoder

def read_contents(*names, **kwargs):
    return io.open(
        os.path.join(*names),
        encoding=kwargs.get("encoding", "utf8")
    ).read()

# 1st try to use the API_KEY environment variable that we encrypted
# in our .travis.yml
api_key = os.environ.get("API_KEY", None)
if not api_key:
	try:
	    api_key = read_contents(os.path.dirname(__file__), '.api_key').strip()
	except IOError as exc:
	    raise ValueError("Google now requires an API key to be provided")

@pytest.mark.webtest
def test_GoogleLocator_WithAPIKey():
    locator = GoogleGeocoder(api_key=api_key)
    l = locator['Eiffel Tower']
    assert l is not None
