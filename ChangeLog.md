# CHANGELOG

## 2.2 - 2020-05-20

### Changed

- Fix for [bug #48](https://github.com/sffjunkie/astral/issues/48). As per the bug report the angle to adjust for the effect of elevation should have been θ (not α).
- The sun functions can now also be passed the timezone as a string. Previously only a pytz timezone was accepted.

## 2.1 - 2020-02-12

### Bug Fix

- Fix for bug #44 - Incorrectly raised exception when UTC sun times were on the day previous to the day asked for. This only manifested itself for timezones with a large positive offset.

## 2.0 - 2020-02-11

### Refactor

- This is a code refactor as well as an update so it is highly likely that you will need to adapt your code to suit.
- Astral, AstralGeocoder & GoogleGeocoder classes removed
- Requires python 3.6+ due to the use of dataclasses
- New LocationInfo class to store a location name, region, timezone, latitude & longitude
- New Observer class to store a latitude, longitude & elevation
- Geocoder database now returns a LocationInfo instead of a Location

## 1.10.1 - 2019-02-06

### Changed

Keywords arguments to Astral **init** are now passed to the geocoder to allow for passing
the `api_key` to GoogleGeocoder.

## 1.10 - 2019-02-04

### Added

Added method to AstralGeocoder to add locations to the database

## 1.9.2 - 2019-01-31

### Changed

Version 1.9 broke the sun_utc method. Sun UTC calculation passed incorrect
parameter to more specific methods e.g. sunrise, sunset etc.

## 1.9.1 - 2019-01-28

### Changed

Corrected version number in module source code.

## 1.9 - 2019-01-28

### Added

Sun calculations now take into account the elevation of the location.

## 1.8 - 2018-12-06

### Added

Added command line interface to return sun information as json.
Added support for no timezone in Location methods.

## 1.7.1 - 2018-10-25

### Changed

Changed GoogleGeocoder test to not use raise...from as this is not valid for Python 2

## 1.7 - 2018-10-24

### Changed

- Requests is now only needed when using GoogleGeocoder
- GoogleGeocoder now requires the `api_key` parameter to be passed to the constructor

## 1.6.1 - 2018-05-02

### Changed

- Updated Travis CI configuration

### Added

- requirements-dev.txt

## 1.6 - 2018-02-22

### Changed

- Added api_key parameter to GoogleGeocoder **init** method. Idea from
    wpietruszewski https://github.com/sffjunkie/astral/pull/12

## 1.5 - 2017-12-07

### Added

- this file

### Changed

- dawn_utc, sunrise_utc, sunset_utc and dusk_utc now only raise AstralError for a math domain
    exception all other exceptions are passed through.
- moon_phase now takes another parameter if the type to return either int (the default) or float
