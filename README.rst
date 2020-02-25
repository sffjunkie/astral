Astral
======

|travis_status| |pypi_ver|

.. |travis_status| image:: https://travis-ci.org/sffjunkie/astral.svg?branch=master
    :target: https://travis-ci.org/sffjunkie/astral

.. |pypi_ver| image:: https://img.shields.io/pypi/v/astral.svg
    :target: https://pypi.org/project/astral/

This is 'astral' a Python module which calculates

    * Sun's position: Solar azimuth, zenith and elevation angles for the specified time.
    * Times for various positions of the sun: dawn, sunrise, solar noon,
      sunset, dusk and solar midnight.
    * Time for the specified elevation of the sun.
    * Periods of the day: blue hour, golden hour, twilight, daylight, night and Rahukaalam.
    * The phase of the moon.

It ships with a geocoder and a starter database of several cities worldwide but can also access Google Maps services for geocoding.

For documentation see the https://astral.readthedocs.io/en/stable/index.html

GoogleGeocoder
~~~~~~~~~~~~~~

`GoogleGeocoder` uses the mapping services provided by Google

Access to the `GoogleGeocoder` requires you to agree to be bound by
Google Maps/Google Earth APIs Terms of Service found at
https://developers.google.com/maps/terms which includes but is not limited to
having a Google Account.

More information on Google's maps service can be found at
https://developers.google.com/maps/documentation/
