import pytest

from astral import GoogleGeocoder

@pytest.mark.webtest
def test_GoogleLocator():
    locator = GoogleGeocoder()
    l = locator['Eiffel Tower']
    assert l is not None

if __name__ == '__main__':
    test_GoogleLocator()
