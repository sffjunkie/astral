.. Copyright 2009-2010, Simon Kennedy, python@sffjunkie.co.uk

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
   .. automethod:: time_at_elevation(self, elevation, direction=SUN_RISING, date=None, local=True)
   .. automethod:: solar_azimuth   
   .. automethod:: solar_elevation   
   .. automethod:: solar_zenith   
   .. automethod:: golden_hour(self, date=None, local=True, direction=SUN_RISING)
   .. automethod:: blue_hour(self, date=None, local=True, direction=SUN_RISING)
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
   

