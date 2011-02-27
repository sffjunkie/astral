from nose.tools import raises

from astral import CityDB

def testGroup():
    db = CityDB()
    e = db.europe
    
@raises(AttributeError)    
def testUnknownGroup():
    db = CityDB()
    e = db.wallyland

def testAllCities():
    db = CityDB()
    cities = db.cities
    cities.sort()
    
    for city_name in cities:
        city = db[city_name]

if __name__ == "__main__":
    testGroup()
    testAllCities()
