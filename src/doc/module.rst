.. Copyright 2009-2019, Simon Kennedy, sffjunkie+code@gmail.com

.. Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

..   http://www.apache.org/licenses/LICENSE-2.0

.. Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

The :mod:`astral` Module
========================

.. automodule:: astral

Astral
------

.. autoclass:: Astral
   :members:
   :member-order: bysource

   .. automethod:: __getitem__

Location
--------

.. autoclass:: Location

   .. automethod:: __init__
   .. autoattribute:: latitude
   .. autoattribute:: longitude
   .. autoattribute:: elevation
   .. autoattribute:: timezone
   .. autoattribute:: tz
   .. autoattribute:: tzinfo
   .. autoattribute:: solar_depression
   .. automethod:: sun
   .. automethod:: dawn
   .. automethod:: sunrise
   .. automethod:: solar_noon
   .. automethod:: sunset
   .. automethod:: dusk
   .. automethod:: daylight
   .. automethod:: night
   .. automethod:: twilight(direction=SUN_RISING, date=None, local=True)
   .. automethod:: golden_hour(direction=SUN_RISING, date=None, local=True)
   .. automethod:: blue_hour(direction=SUN_RISING, date=None, local=True)
   .. automethod:: time_at_elevation(elevation, direction=SUN_RISING, date=None, local=True)
   .. automethod:: solar_azimuth
   .. automethod:: solar_elevation
   .. automethod:: solar_zenith
   .. automethod:: moon_phase
   .. automethod:: rahukaalam

Geocoders
---------

.. autoclass:: AstralGeocoder
   :members:
   :member-order: bysource

.. autoclass:: GoogleGeocoder
   :members:
   :member-order: bysource


