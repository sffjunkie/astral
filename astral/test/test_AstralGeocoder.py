# -*- coding: utf-8 -*-
from nose.tools import raises

from astral import AstralGeocoder

def test_Group():
    db = AstralGeocoder()
    _e = db.europe
    
@raises(AttributeError)    
def test_UnknownGroup():
    db = AstralGeocoder()
    _e = db.wallyland

def test_CityContainment():
    db = AstralGeocoder()
    assert 'london' in db

def test_GroupContainment():
    db = AstralGeocoder()
    assert 'africa' in db

def test_CityCountry():
    city_name = 'Birmingham,England'
    
    db = AstralGeocoder()
    city = db[city_name]
    assert city.name == 'Birmingham'
    assert city.region == 'England'

def test_MultiCountry():
    db = AstralGeocoder()
    city = db['Abu Dhabi']
    assert city.name == 'Abu Dhabi'

def test_MultiCountryWithCountry():
    """Test for fix made due to bug report from Klaus Alexander Seistrup"""
    
    db = AstralGeocoder()
    city = db['Abu Dhabi,United Arab Emirates']
    assert city.name == 'Abu Dhabi'

    city = db['Abu Dhabi,UAE']
    assert city.name == 'Abu Dhabi'

def test_Adelaide():
    """Test for fix made due to bug report from Klaus Alexander Seistrup"""
    
    db = AstralGeocoder()
    _city = db['Adelaide']

def test_AllCities():
    db = AstralGeocoder()
    locations = db.locations
    locations.sort()
    
    for city_name in locations:
        _city = db[city_name]

if __name__ == "__main__":
    test_CityCountry()
    test_MultiCountry()
    test_Adelaide()
    test_Group()
    test_CityContainment()
    test_GroupContainment()
    test_AllCities()

