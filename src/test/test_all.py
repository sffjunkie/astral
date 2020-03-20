from astral.geocoder import all_locations
from astral.sun import sun

def test_AllLocations(test_database):
    for location in all_locations(test_database):
        sun(location.observer)
