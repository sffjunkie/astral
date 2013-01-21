from astral import GoogleGeocoder

def test_GoogleLocator():
    locator = GoogleGeocoder()
    l = locator['Eiffel Tower']
    

if __name__ == '__main__':
    test_GoogleLocator()
