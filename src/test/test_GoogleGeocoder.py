import io
import os.path
import pytest

from astral import GoogleGeocoder

@pytest.mark.webtest
def test_GoogleLocator():
    locator = GoogleGeocoder()
    l = locator['Eiffel Tower']
    assert l is not None

def read_contents(*names, **kwargs):
    return io.open(
        os.path.join(*names),
        encoding=kwargs.get("encoding", "utf8")
    ).read()

api_key = read_contents(os.path.dirname(__file__), '.api_key')
@pytest.mark.webtest
def test_GoogleLocator_WithAPIKey():
    if api_key:
        locator = GoogleGeocoder(api_key=api_key)
        l = locator['Eiffel Tower']
        assert l is not None
    else:
        raise AssertionError('api_key not found')


if __name__ == '__main__':
    test_GoogleLocator()
