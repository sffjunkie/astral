from nose.tools import raises

from astral import CityDB

def testGroup():
    db = CityDB()
    e = db.europe
    
@raises(AttributeError)    
def testUnknownGroup():
    db = CityDB()
    e = db.wallyland

def testCityContainment():
    db = CityDB()
    assert 'london' in db

def testGroupContainment():
    db = CityDB()
    assert 'africa' in db

def testAllCities():
    db = CityDB()
    cities = db.cities
    cities.sort()
    
    for city_name in cities:
        city = db[city_name]

if __name__ == "__main__":
    testGroup()
    testCityContainment()
    testGroupContainment()
    testAllCities()
