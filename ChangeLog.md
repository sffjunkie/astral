# CHANGELOG

## 1.6.1 - 2018-05-02
### Changed
- Updated Travis CI configuration

### Added
- requirements-dev.txt

## 1.6 - 2018-02-22
### Changed
- Added api_key parameter to GoogleGeocoder __init__ method. Idea from wpietruszewski https://github.com/sffjunkie/astral/pull/12

## 1.5 - 2017-12-07
### Added
- this file

### Changed
- dawn_utc, sunrise_utc, sunset_utc and dusk_utc now only raise AstralError for a math domain exception all other exceptions are passed through.
- moon_phase now takes another parameter if the type to return either int (the default) or float
