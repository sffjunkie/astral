# CHANGELOG

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

- Added api_key parameter to GoogleGeocoder __init__ method. Idea from
  wpietruszewski https://github.com/sffjunkie/astral/pull/12

## 1.5 - 2017-12-07

### Added

- this file

### Changed

- dawn_utc, sunrise_utc, sunset_utc and dusk_utc now only raise AstralError for a math domain
  exception all other exceptions are passed through.
- moon_phase now takes another parameter if the type to return either int (the default) or float
