.. Copyright 2009-2014, Simon Kennedy, sffjunkie+code@gmail.com

Astral v\ |release|
===================

Astral is a python module for calculating the times of various aspects of
the sun and moon.

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

The following example demonstrates the functionality available in the module::

    >>> import datetime
    >>> from astral import Astral
    
    >>> city_name = 'London'
    
    >>> a = Astral()
    >>> a.solar_depression = 'civil'
    
    >>> city = a[city_name]
    
    >>> print('Information for %s/%s\n' % (city_name, city.region))
    Information for London/England
    
    >>> timezone = city.timezone
    >>> print('Timezone: %s' % timezone)
    Timezone: Europe/London
    
    >>> print('Latitude: %.02f; Longitude: %.02f\n' % \
    >>>     (city.latitude, city.longitude))
    Latitude: 51.60; Longitude: 0.08
    
    >>> sun = city.sun(date=datetime.date(2009, 4, 22), local=True)
    >>> print('Dawn:    %s' % str(sun['dawn']))
    >>> print('Sunrise: %s' % str(sun['sunrise']))
    >>> print('Noon:    %s' % str(sun['noon']))
    >>> print('Sunset:  %s' % str(sun['sunset']))
    >>> print('Dusk:    %s' % str(sun['dusk']))
    Dawn:     2009-04-22 05:12:56+01:00
    Sunrise:  2009-04-22 05:49:36+01:00
    Noon:     2009-04-22 12:58:48+01:00
    Sunset:   2009-04-22 20:09:07+01:00
    Dusk:     2009-04-22 20:45:52+01:00

Access to the current geocoder can be made through the Astral class::
    
    >>> a = Astral()
    >>> geo = a.geocoder
    >>> london = geo['London']
    
Timezone groups such as Europe can be accessed via attributes on the
:class:`~astral.AstralGeocoder`::
    
    >>> geo = AstralGeocoder()
    >>> europe = geo.europe.locations
    >>> europe.sort()
    >>> europe
    ['Aberdeen', 'Amsterdam', 'Andorra la Vella', 'Ankara', 'Athens', ...]


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
    
Or you can use :command:`pip`::

    pip install astral

Cities
======

The module includes location and time zone data for the following cities.
The list includes all capital cities plus some from the UK. The list also
includes the US state capitals and some other US cities.

Aberdeen, Abu Dhabi, Abu Dhabi, Abuja, Accra, Addis Ababa, Adelaide, Al Jubail,
Albany, Albuquerque, Algiers, Amman, Amsterdam, Anchorage, Andorra la Vella,
Ankara, Annapolis, Antananarivo, Apia, Ashgabat, Asmara, Astana, Asuncion,
Athens, Atlanta, Augusta, Austin, Avarua, Baghdad, Baku, Baltimore, Bamako,
Bandar Seri Begawan, Bangkok, Bangui, Banjul, Barrow-In-Furness, Basse-Terre,
Basseterre, Baton Rouge, Beijing, Beirut, Belfast, Belgrade, Belmopan, Berlin,
Bern, Billings, Birmingham, Birmingham, Bishkek, Bismarck, Bissau, Bloemfontein,
Bogota, Boise, Bolton, Boston, Bradford, Brasilia, Bratislava, Brazzaville,
Bridgeport, Bridgetown, Brisbane, Bristol, Brussels, Bucharest, Bucuresti,
Budapest, Buenos Aires, Buffalo, Bujumbura, Burlington, Cairo, Canberra, Cape
Town, Caracas, Cardiff, Carson City, Castries, Cayenne, Charleston, Charlotte,
Charlotte Amalie, Cheyenne, Chicago, Chisinau, Cleveland, Columbia, Columbus,
Conakry, Concord, Copenhagen, Cotonou, Crawley, Dakar, Dallas, Damascus, Dammam,
Denver, Des Moines, Detroit, Dhaka, Dili, Djibouti, Dodoma, Doha, Douglas,
Dover, Dublin, Dushanbe, Edinburgh, El Aaiun, Fargo, Fort-de-France, Frankfort,
Freetown, Funafuti, Gaborone, George Town, Georgetown, Gibraltar, Glasgow,
Greenwich, Guatemala, Hanoi, Harare, Harrisburg, Hartford, Havana, Helena,
Helsinki, Hobart, Hong Kong, Honiara, Honolulu, Houston, Indianapolis,
Islamabad, Jackson, Jacksonville, Jakarta, Jefferson City, Jerusalem, Juba,
Jubail, Juneau, Kabul, Kampala, Kansas City, Kathmandu, Khartoum, Kiev, Kigali,
Kingston, Kingston, Kingstown, Kinshasa, Koror, Kuala Lumpur, Kuwait, La Paz,
Lansing, Las Vegas, Leeds, Leicester, Libreville, Lilongwe, Lima, Lincoln,
Lisbon, Little Rock, Liverpool, Ljubljana, Lome, London, Los Angeles,
Louisville, Luanda, Lusaka, Luxembourg, Macau, Madinah, Madison, Madrid, Majuro,
Makkah, Malabo, Male, Mamoudzou, Managua, Manama, Manchester, Manchester,
Manila, Maputo, Maseru, Masqat, Mbabane, Mecca, Medina, Memphis, Mexico, Miami,
Milwaukee, Minneapolis, Minsk, Mogadishu, Monaco, Monrovia, Montevideo,
Montgomery, Montpelier, Moroni, Moscow, Moskva, Mumbai, Muscat, N'Djamena,
Nairobi, Nashville, Nassau, Naypyidaw, New Delhi, New Orleans, New York, Newark,
Newcastle, Newcastle Upon Time, Ngerulmud, Niamey, Nicosia, Norwich, Nouakchott,
Noumea, Nuku'alofa, Nuuk, Oklahoma City, Olympia, Omaha, Oranjestad, Orlando,
Oslo, Ottawa, Ouagadougou, Oxford, P'yongyang, Pago Pago, Palikir, Panama,
Papeete, Paramaribo, Paris, Perth, Philadelphia, Phnom Penh, Phoenix, Pierre,
Plymouth, Podgorica, Port Louis, Port Moresby, Port of Spain, Port-Vila,
Port-au-Prince, Portland, Portland, Porto-Novo, Portsmouth, Prague, Praia,
Pretoria, Pristina, Providence, Quito, Rabat, Raleigh, Reading, Reykjavik,
Richmond, Riga, Riyadh, Road Town, Rome, Roseau, Sacramento, Saint Helier, Saint
Paul, Saint Pierre, Saipan, Salem, Salt Lake City, San Diego, San Francisco, San
Jose, San Juan, San Marino, San Salvador, Sana, Sana'a, Santa Fe, Santiago,
Santo Domingo, Sao Tome, Sarajevo, Seattle, Seoul, Sheffield, Singapore, Sioux
Falls, Skopje, Sofia, Southampton, Springfield, Sri Jayawardenapura Kotte, St.
George's, St. John's, St. Peter Port, Stanley, Stockholm, Sucre, Suva, Swansea,
Swindon, Sydney, T'bilisi, Taipei, Tallahassee, Tallinn, Tarawa, Tashkent,
Tbilisi, Tegucigalpa, Tehran, Thimphu, Tirana, Tirane, Tokyo, Toledo, Topeka,
Torshavn, Trenton, Tripoli, Tunis, Ulaanbataar, Ulan Bator, Vaduz, Valletta,
Vienna, Vientiane, Vilnius, Virginia Beach, W. Indies, Warsaw, Washington DC,
Wellington, Wichita, Willemstad, Wilmington, Windhoek, Wolverhampton,
Yamoussoukro, Yangon, Yaounde, Yaren, Yerevan, Zagreb

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
    
Simon Kennedy <sffjunkie+code@gmail.com>
    
Version History
===============

======== =======================================================================
Version  Description
======== =======================================================================
0.7.4    Added Canadian cities from Yip Shing Ho
-------- -----------------------------------------------------------------------
0.7.3    Fix for bug `1239387`_ submitted by Torbjörn Lönnemark
-------- -----------------------------------------------------------------------
0.7.2    Minor bug fix in :class:`~astral.GoogleGeocoder`. location name and
         region are now stripped of whitespace
-------- -----------------------------------------------------------------------
0.7.1    Bug fix. Missed a vital return statement in the
         :class:`~astral.GoogleGeocoder`
-------- -----------------------------------------------------------------------
0.7      * Added ability to lookup location information from
           Google's mapping APIs (see :class:`~astral.GoogleGeocoder`) 
         * Renamed :class:`City` class to :class:`~astral.Location`
         * Renamed :class:`CityDB` to :class:`~astral.AstralGeocoder`
         * Added elevations of cities to database and property to
           obtain elevation from :class:`~astral.Location` class
-------- -----------------------------------------------------------------------
0.6.2    Added various cities to database as per https://bugs.launchpad.net/astral/+bug/1040936
-------- -----------------------------------------------------------------------
0.6.1    * Docstrings were not updated to match changes to code.
         * Other minor docstring changes made
-------- -----------------------------------------------------------------------
0.6      * Fix for bug `884716`_ submitted by Martin Heemskerk
           regarding moon phase calculations
           
         * Fixes for bug report `944754`_ submitted by Hajo Werder
         
           - Changed co-ordinate system so that eastern longitudes
             are now positive
           - Added solar_depression property to City class
-------- -----------------------------------------------------------------------
0.5      * Changed :class:`City` to accept unicode name and country.
         * Moved city information into a database class :class:`CityDB`
         * Added attribute access to database for timezone groups
-------- -----------------------------------------------------------------------
0.4      * Duplicate city names could not be accessed.
         * Sun calculations for some cities failed with times
           outside valid ranges.
         * Fixes for city data.
         * Added calculation for moon phase.
-------- -----------------------------------------------------------------------
0.3      * Changed to `Apache`_ V2.0 license.
         * Fix for bug `555508`_ submitted by me.
         * US state capitals and other cities added.
-------- -----------------------------------------------------------------------
0.2      Fix for bug `554041`_ submitted by Derek\_ / John Dimatos 
-------- -----------------------------------------------------------------------
0.1      First release
======== =======================================================================

.. _Rahukaalam: http://en.wikipedia.org/wiki/Rahukaalam
.. _Sourceforge: http://pytz.sourceforge.net/
.. _easy_install: http://peak.telecommunity.com/DevCenter/EasyInstall
.. _Apache: http://www.opensource.org/licenses/apache2.0.php
.. _Sphinx: http://sphinx.pocoo.org/
.. _554041: https://bugs.launchpad.net/astral/+bug/554041
.. _555508: https://bugs.launchpad.net/astral/+bug/555508
.. _884716: https://bugs.launchpad.net/astral/+bug/884716
.. _944754: https://bugs.launchpad.net/astral/+bug/944754
.. _1239387: https://bugs.launchpad.net/astral/+bug/1239387
.. _javascript: http://www.skyandtelescope.com/observing/objects/javascript/moon_phases
    

.. toctree::
   :maxdepth: 2
   :hidden:
   
   module
