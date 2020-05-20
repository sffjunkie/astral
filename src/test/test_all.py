from astral.geocoder import all_locations
from astral.sun import noon

def test_AllLocations(test_database):
    for location in all_locations(test_database):
        noon(location.observer)
