.. Copyright 2009-2010, Simon Kennedy, python@sffjunkie.co.uk
   Distributed under the terms of the MIT License.

Welcome to Astral
=================

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

This module is licensed under the terms of the `MIT`_ license.
    
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
The list includes all capital cities plus some from the UK.

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

Thanks
======

The sun calculations in this module were adapted, for Python, from the following
spreadsheet.
    
    http://www.ecy.wa.gov/programs/eap/models/twilight.zip
    
Which takes its calculations from

    http://www.srrb.noaa.gov/highlights/sunrise/azel.html

Also to `Sphinx`_ for making doc generation an easy thing (not that the writing
of the docs is any easier.)

Contact
=======
    
Simon Kennedy <python@sffjunkie.co.uk>
    
Version History
===============

======== ==========================================
Version  Description
======== ==========================================
0.1      First release
-------- ------------------------------------------
0.2      Fix for bug `554041`_ submitted by Derek\_ 
======== ==========================================

.. _Rahukaalam: http://en.wikipedia.org/wiki/Rahukaalam
.. _Sourceforge: http://pytz.sourceforge.net/
.. _easy_install: http://peak.telecommunity.com/DevCenter/EasyInstall
.. _MIT: http://www.opensource.org/licenses/mit-license.html
.. _Sphinx: http://sphinx.pocoo.org/
.. _554041: https://bugs.launchpad.net/astral/+bug/554041

    
.. toctree::
   :maxdepth: 2
   :hidden:
   
   module

