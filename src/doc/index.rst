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

Welcome to Astral V0.4
======================

Astral is a python module for calculating the times of various aspects of
the sun.

It calculates the following

Dawn
    The time in the morning when the sun is a specific number of degrees
    below the horizon.

Sunrise
    The time in the morning when the top of the sun breaks the horizon
    (asuming a location with no obscuring features.)
    
Solar Noon
    The time when the sun is at its highest point.
    
Sunset
    The time in the evening when the sun is about to disappear below the horizon
    (asuming a location with no obscuring features.)

Dusk
    The time in the evening when the sun is a specific number of degrees
    below the horizon.

Solar Azimuth
    The number of degrees clockwise from North at which the sun can be seen

Solar Elevation
    The number of degrees up from the horizon at which the sun can be seen

`Rahukaalam`_
    "Rahukaalam or the period of Rahu is a certain amount of time every day
    that is considered inauspicious for any new venture according to Indian
    astrology".
    
Moon Phase
    Calculates the phase of the moon for a specified date.

Example
=======

The following example demonstrates the functionality available in the module

.. code-block:: python

    import datetime
    from astral import Astral
    
    city_name = 'London'
    
    a = Astral()
    a.solar_depression = 'civil'
    
    city = a[city_name]
    
    print('Information for %s/%s\n' % (city_name, city.country))
    
    timezone = city.timezone
    print('Timezone: %s' % timezone)
    
    print('Latitude: %.02f; Longitude: %.02f\n' % \
        (city.latitude, city.longitude))
    
    sun = city.sun(date=datetime.date(2009, 4, 22), local=True)
    print('Dawn:    %s' % str(sun['dawn']))
    print('Sunrise: %s' % str(sun['sunrise']))
    print('Noon:    %s' % str(sun['noon']))
    print('Sunset:  %s' % str(sun['sunset']))
    print('Dusk:    %s' % str(sun['dusk']))

Produces the following output::

    Information for London/England
    
    Timezone: Europe/London
    Latitude: 51.60; Longitude: 0.08
    
    Dawn:     2009-04-22 05:12:56+01:00
    Sunrise:  2009-04-22 05:49:36+01:00
    Noon:     2009-04-22 12:58:48+01:00
    Sunset:   2009-04-22 20:09:07+01:00
    Dusk:     2009-04-22 20:45:52+01:00

License
=======

This module is licensed under the terms of the `Apache`_ V2.0 license.
    
Dependencies
============

Astral has one external dependency on 'pytz' which can either be obtained
from `Sourceforge`_ page or via the `easy_install`_ method, whichever is your
particular poison.

Installation
============

When you've added the pytz package to install astral unzip the archive to
a handy location and execute the standard Python installation method::
    
    python setup.py install

Cities
======

The module includes location and time zone data for the following cities.
The list includes all capital cities plus some from the UK. The list also
includes the US state capitals and some other US cities.

Aberdeen, Abu Dhabi, Abuja, Accra, Addis Ababa, Adelaide, Al Jubail, Algiers,
Amman, Amsterdam, Andorra la Vella, Ankara, Antananarivo, Apia, Ashgabat,
Asmara, Astana, Asuncion, Athens, Baghdad, Baku, Bamako, Bandar Seri Begawan,
Bangkok, Bangui, Banjul, Basse-Terre, Basseterre, Beijing, Beirut, Belgrade,
Belmopan, Berlin, Bern, Birmingham, Bishkek, Bissau, Bloemfontein, Bogota,
Bolton, Bradford, Brasilia, Bratislava, Brazzaville, Bridgetown, Brisbane,
Bristol, Brussels, Bucharest, Bucuresti, Budapest, Buenos Aires, Bujumbura,
Cairo, Canberra, Cape Town, Caracas, Cardiff, Castries, Cayenne, Charlotte
Amalie, Chisinau, Conakry, Copenhagen, Cotonou, Crawley, Dakar, Damascus, Dammam, Dhaka,
Dili, Djibouti, Dodoma, Doha, Dublin, Dushanbe, Edinburgh, Fort-de-France,
Freetown, Funafuti, Gaborone, George Town, Georgetown, Glasgow, Guatemala,
Hanoi, Harare, Havana, Helsinki, Hobart, Honiara, Islamabad, Jakarta, Jerusalem, Jubail,
Kabul, Kampala, Kathmandu, Khartoum, Kiev, Kigali, Kingston, Kingstown,
Kinshasa, Koror, Kuala Lumpur, Kuwait, La Paz, Leeds, Leicester, Libreville,
Lilongwe, Lima, Lisbon, Liverpool, Ljubljana, Lome, London, Luanda, Lusaka,
Luxembourg, Macau, Madinah, Madrid, Makkah, Malabo, Male, Mamoudzou, Managua,
Manama, Manchester, Manila, Maputo, Maseru, Masqat, Mbabane, Mecca, Medina,
Mexico, Minsk, Mogadishu, Monrovia, Montevideo, Moroni, Moscow, Moskva,
N'Djamena, Nairobi, Nassau, New Delhi, Newcastle, Newcastle Upon Time, Niamey,
Nicosia, Norwich, Nouakchott, Noumea, Nuku'alofa, Nuuk, Oranjestad, Oslo,
Ottawa, Ouagadougou, Oxford, P'yongyang, Pago Pago, Palikir, Panama, Papeete,
Paramaribo, Paris, Perth, Phnom Penh, Plymouth, Port Moresby, Port-Vila,
Port-au-Prince, Porto-Novo, Portsmouth, Prague, Praia, Pretoria, Quito, Reading,
Reykjavik, Riga, Riyadh, Road Town, Rome, Roseau, Saint Pierre, Saipan, San
Jose, San Juan, San Marino, San Salvador, Santiago, Santo Domingo, Sao Tome,
Sarajevo, Seoul, Sheffield, Skopje, Sofia, Southampton, St. Peter Port, Stanley,
Stockholm, Sucre, Suva, Swansea, Swindon, Sydney, T'bilisi, Tallinn, Tarawa,
Tashkent, Tegucigalpa, Tehran, Thimphu, Tirane, Torshavn, Tripoli, Tunis, Vaduz,
Valletta, Vienna, Vientiane, Vilnius, W. Indies, Warsaw, Washington DC,
Wellington, Willemstad, Windhoek, Wolverhampton, Yamoussoukro, Yangon, Yaounde,
Yerevan, Zagreb

US Cities
---------

Albany, Albuquerque, Anchorage, Annapolis, Atlanta, Augusta, Austin, Baltimore,
Baton Rouge, Billings, Birmingham, Bismarck, Boise, Boston, Bridgeport, Buffalo,
Burlington, Carson City, Charleston, Charlotte, Cheyenne, Chicago, Cleveland,
Columbia, Columbus, Concord, Dallas, Denver, Des Moines, Detroit, Dover, Fargo,
Frankfort, Harrisburg, Hartford, Helena, Honolulu, Houston, Indianapolis,
Jackson, Jacksonville, Jefferson City, Juneau, Kansas City, Lansing, Las Vegas,
Lincoln, Little Rock, Los Angeles, Louisville, Madison, Manchester, Memphis,
Miami, Milwaukee, Minneapolis, Montgomery, Montpelier, Nashville, New Orleans,
New York, Newark, Oklahoma City, Olympia, Omaha, Orlando, Philadelphia, Phoenix,
Pierre, Portland, Portland, Providence, Raleigh, Richmond, Sacramento, Saint
Paul, Salem, Salt Lake City, San Diego, San Francisco, Santa Fe, Seattle, Sioux
Falls, Springfield, Tallahassee, Toledo, Topeka, Trenton, Virginia Beach,
Wichita, Wilmington

Thanks
======

The sun calculations in this module were adapted, for Python, from the following
spreadsheet.
    
    http://www.ecy.wa.gov/programs/eap/models/twilight.zip
    
Which takes its calculations from

    http://www.srrb.noaa.gov/highlights/sunrise/azel.html
    
The moon phase calculation is based on some `javascript`_ code
from Sky and Telescope magazine

    | Moon-phase calculation
    | Roger W. Sinnott, Sky & Telescope, June 16, 2006.

Also to `Sphinx`_ for making doc generation an easy thing (not that the writing
of the docs is any easier.)

Contact
=======
    
Simon Kennedy <python@sffjunkie.co.uk>
    
Version History
===============

======== =========================================================
Version  Description
======== =========================================================
0.1      First release
-------- ---------------------------------------------------------
0.2      Fix for bug `554041`_ submitted by Derek\_ / John Dimatos 
-------- ---------------------------------------------------------
0.3      * Changed to `Apache`_ V2.0 license.
         * Fix for bug `555508`_ submitted by me.
         * US state capitals and other cities added.
-------- ---------------------------------------------------------
0.4      * Duplicate city names could not be accessed.
         * Sun calculations for some cities failed with times
           outside valid ranges.
         * Fixes for city data.
         * Added calculation for moon phase.
======== =========================================================

.. _Rahukaalam: http://en.wikipedia.org/wiki/Rahukaalam
.. _Sourceforge: http://pytz.sourceforge.net/
.. _easy_install: http://peak.telecommunity.com/DevCenter/EasyInstall
.. _Apache: http://www.opensource.org/licenses/apache2.0.php
.. _Sphinx: http://sphinx.pocoo.org/
.. _554041: https://bugs.launchpad.net/astral/+bug/554041
.. _555508: https://bugs.launchpad.net/astral/+bug/555508
.. _javascript: http://www.skyandtelescope.com/observing/objects/javascript/moon_phases

    
.. toctree::
   :maxdepth: 2
   :hidden:
   
   module
