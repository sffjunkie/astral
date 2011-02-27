# -*- coding: utf-8 -*-
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

def testCityCountry():
    city_name = 'Birmingham,England'
    
    db = CityDB()
    city = db[city_name]
    assert city.name == 'Birmingham'
    assert city.country == 'England'

def testMultiCountry():
    db = CityDB()
    city = db['Abu Dhabi']
    assert city.name == 'Abu Dhabi'

def testMultiCountryWithCountry():
    """Test for fix made due to bug report from Klaus Alexander Seistrup"""
    
    db = CityDB()
    city = db['Abu Dhabi,United Arab Emirates']
    assert city.name == 'Abu Dhabi'

    city = db['Abu Dhabi,UAE']
    assert city.name == 'Abu Dhabi'

def testAdelaide():
    """Test for fix made due to bug report from Klaus Alexander Seistrup"""
    
    db = CityDB()
    city = db['Adelaide']

def testAllCities():
    db = CityDB()
    cities = db.cities
    cities.sort()
    
    for city_name in cities:
        city = db[city_name]

if __name__ == "__main__":
    testCityCountry()
    testMultiCountry()
    testAdelaide()
    testGroup()
    testCityContainment()
    testGroupContainment()
    testAllCities()
