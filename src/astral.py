# -*- coding: utf-8 -*-
#
# Copyright 2009-2010, Simon Kennedy, python@sffjunkie.co.uk
# Distributed under the terms of the MIT License.

"""
The :mod:`astral` module provides the means to calculate dawn, sunrise,
solar noon, sunset, dusk and rahukaalam times, plus solar azimuth and elevation,
for specific cities or at a specific latitude/longitude.

It provides 2 main classes :class:`Astral` and :class:`City`.

:class:`Astral`
    Has 2 main capabilities

    * Calculates the events in the UTC timezone.
    * Holds a dictionary of City classes to provide information and
      calculations for a specific city.
    
:class:`City`
    Holds information about a city and provides functions to calculate
    the event times for the city in the correct time zone.

For example

>>> from astral import *
>>> a = Astral()
>>> city = a['London']
>>> print('Information for %s' % city.name)
Information for London
>>> timezone = city.timezone
>>> print('Timezone: %s' % timezone)
Timezone: Europe/London
>>> print('Latitude: %.02f; Longitude: %.02f' % (city.latitude, city.longitude))
Latitude: 51.60; Longitude: 0.08
>>> sun = city.sun(local=True)
>>> print('Dawn:    %s' % str(sun['dawn']))
Dawn:    2009-04-22 05:12:56+01:00
"""

import datetime
from math import cos, sin, tan, acos, asin, atan2, floor, radians, degrees

try:
    import pytz
except ImportError:
    raise ImportError('The astral module requires the pytz module to be available.')

__all__ = ['City', 'Astral','AstralError']

__version__ = "0.2"
__author__ = "Simon Kennedy <python@sffjunkie.co.uk>"

_CITY_INFO = """
Abu Dhabi,UAE,24°28'N,54°22'E,Asia/Dubai
Abu Dhabi,United Arab Emirates,24°28'N,54°22'E,Asia/Dubai
Abuja,Nigeria,09°05'N,07°32'E,Africa/Lagos
Accra,Ghana,05°35'N,00°06'W,Africa/Accra
Addis Ababa,Ethiopia,09°02'N,38°42'E,Africa/Addis_Ababa
Adelaide,Australia,34°56'S,138°36'E,Australia/Adelaide
Al Jubail,Saudi Arabia,25°24'N,49°39'W,Asia/Riyadh
Algiers,Algeria,36°42'N,03°08'E,Africa/Algiers
Amman,Jordan,31°57'N,35°52'E,Asia/Amman
Amsterdam,Netherlands,52°23'N,04°54'E,Europe/Amsterdam
Andorra la Vella,Andorra,42°31'N,01°32'E,Europe/Andorra
Ankara,Turkey,39°57'N,32°54'E,Europe/Istanbul
Antananarivo,Madagascar,18°55'S,47°31'E,Indian/Antananarivo
Apia,Samoa,13°50'S,171°50'W,Pacific/Apia
Ashgabat,Turkmenistan,38°00'N,57°50'E,Asia/Ashgabat
Asmara,Eritrea,15°19'N,38°55'E,Africa/Asmara
Astana,Kazakhstan,51°10'N,71°30'E,Asia/Qyzylorda
Asuncion,Paraguay,25°10'S,57°30'W,America/Asuncion
Athens,Greece,37°58'N,23°46'E,Europe/Athens
Baghdad,Iraq,33°20'N,44°30'E,Asia/Baghdad
Baku,Azerbaijan,40°29'N,49°56'E,Asia/Baku
Bamako,Mali,12°34'N,07°55'W,Africa/Bamako
Bandar Seri Begawan,Brunei Darussalam,04°52'N,115°00'E,Asia/Brunei
Bangkok,Thailand,13°45'N,100°35'E,Asia/Bangkok
Bangui,Central African Republic,04°23'N,18°35'E,Africa/Bangui
Banjul,Gambia,13°28'N,16°40'W,Africa/Banjul
Basse-Terre,Guadeloupe,16°00'N,61°44'W,America/Guadeloupe
Basseterre,Saint Kitts and Nevis,17°17'N,62°43'W,America/St_Kitts
Beijing,China,39°55'N,116°20'E,Asia/Harbin
Beirut,Lebanon,33°53'N,35°31'E,Asia/Beirut
Belgrade,Yugoslavia,44°50'N,20°37'E,Europe/Belgrade
Belmopan,Belize,17°18'N,88°30'W,America/Belize
Berlin,Germany,52°30'N,13°25'E,Europe/Berlin
Bern,Switzerland,46°57'N,07°28'E,Europe/Zurich
Bishkek,Kyrgyzstan,42°54'N,74°46'E,Asia/Bishkek
Bissau,Guinea-Bissau,11°45'N,15°45'W,Africa/Bissau
Bloemfontein,South Africa,29°12'S,26°07'E,Africa/Johannesburg
Bogota,Colombia,04°34'N,74°00'W,America/Bogota
Brasilia,Brazil,15°47'S,47°55'W,Brazil/East
Bratislava,Slovakia,48°10'N,17°07'E,Europe/Bratislava
Brazzaville,Congo,04°09'S,15°12'E,Africa/Brazzaville
Bridgetown,Barbados,13°05'N,59°30'W,America/Barbados
Brisbane,Australia,27°30'S,153°01'E,Australia/Brisbane
Brussels,Belgium,50°51'N,04°21'E,Europe/Brussels
Bucharest,Romania,44°27'N,26°10'E,Europe/Bucharest
Bucuresti,Romania,44°27'N,26°10'E,Europe/Bucharest
Budapest,Hungary,47°29'N,19°05'E,Europe/Budapest
Buenos Aires,Argentina,36°30'S,60°00'W,America/Argentina/Buenos_Aires
Bujumbura,Burundi,03°16'S,29°18'E,Africa/Bujumbura
Cairo,Egypt,30°01'N,31°14'E,Africa/Cairo
Canberra,Australia,35°15'S,149°08'E,Australia/Canberra
Cape Town,South Africa,33°55'S,18°22'E,Africa/Johannesburg
Caracas,Venezuela,10°30'N,66°55'W,America/Caracas
Castries,Saint Lucia,14°02'N,60°58'W,America/St_Lucia
Cayenne,French Guiana,05°05'N,52°18'W,America/Cayenne
Charlotte Amalie,United States of Virgin Islands,18°21'N,64°56'W,America/Virgin
Chisinau,Moldova,47°02'N,28°50'E,Europe/Chisinau
Conakry,Guinea,09°29'N,13°49'W,Africa/Conakry
Copenhagen,Denmark,55°41'N,12°34'E,Europe/Copenhagen
Cotonou,Benin,06°23'N,02°42'E,Africa/Porto-Novo
Dakar,Senegal,14°34'N,17°29'W,Africa/Dakar
Damascus,Syrian Arab Republic,33°30'N,36°18'E,Asia/Damascus
Dammam,Saudi Arabia,26°30'N,50°12'E,Asia/Riyadh
Dhaka,Bangladesh,23°43'N,90°26'E,Asia/Dhaka
Dili,East Timor,08°29'S,125°34'E,Asia/Dili
Djibouti,Djibouti,11°08'N,42°20'E,Africa/Djibouti
Dodoma,United Republic of Tanzania,06°08'S,35°45'E,Africa/Dar_es_Salaam
Doha,Qatar,25°15'N,51°35'E,Asia/Qatar
Dublin,Ireland,53°21'N,06°15'W,Europe/Dublin
Dushanbe,Tajikistan,38°33'N,68°48'E,Asia/Dushanbe
Fort-de-France,Martinique,14°36'N,61°02'W,America/Martinique
Freetown,Sierra Leone,08°30'N,13°17'W,Africa/Freetown
Funafuti,Tuvalu,08°31'S,179°13'E,Pacific/Funafuti
Gaborone,Botswana,24°45'S,25°57'E,Africa/Gaborone
George Town,Cayman Islands,19°20'N,81°24'W,America/Cayman
Georgetown,Guyana,06°50'N,58°12'W,America/Guyana
Guatemala,Guatemala,14°40'N,90°22'W,America/Guatemala
Hanoi,Viet Nam,21°05'N,105°55'E,Asia/Saigon
Harare,Zimbabwe,17°43'S,31°02'E,Africa/Harare
Havana,Cuba,23°08'N,82°22'W,America/Havana
Helsinki,Finland,60°15'N,25°03'E,Europe/Helsinki
Hobart,Tasmania,42°53'S,147°19'E,Australia/Hobart
Honiara,Solomon Islands,09°27'S,159°57'E,Pacific/Guadalcanal
Islamabad,Pakistan,33°40'N,73°10'E,Asia/Karachi
Jakarta,Indonesia,06°09'S,106°49'E,Asia/Jakarta
Jerusalem,Israel,31°47'N,35°12'E,Asia/Jerusalem
Jubail,Saudi Arabia,27°02'N,49°39'E,Asia/Riyadh
Kabul,Afghanistan,34°28'N,69°11'E,Asia/Kabul
Kampala,Uganda,00°20'N,32°30'E,Africa/Kampala
Kathmandu,Nepal,27°45'N,85°20'E,Asia/Kathmandu
Khartoum,Sudan,15°31'N,32°35'E,Africa/Khartoum
Kiev,Ukraine,50°30'N,30°28'E,Europe/Kiev
Kigali,Rawanda,01°59'S,30°04'E,Africa/Kigali
Kingston,Jamaica,18°00'N,76°50'W,America/Jamaica
Kingston,Norfolk Island,45°20'S,168°43'E,Pacific/Norfolk
Kingstown,Saint vincent and the Grenadines,13°10'N,61°10'W,America/St_Vincent
Kinshasa,Democratic Republic of the Congo,04°20'S,15°15'E,Africa/Kinshasa
Koror,Palau,07°20'N,134°28'E,Pacific/Palau
Kuala Lumpur,Malaysia,03°09'N,101°41'E,Asia/Kuala_Lumpur
Kuwait,Kuwait,29°30'N,48°00'E,Asia/Kuwait
La Paz,Bolivia,16°20'S,68°10'W,America/La_Paz
Libreville,Gabon,00°25'N,09°26'E,Africa/Libreville
Lilongwe,Malawi,14°00'S,33°48'E,Africa/Blantyre
Lima,Peru,12°00'S,77°00'W,America/Lima
Lisbon,Portugal,38°42'N,09°10'W,Europe/Lisbon
Ljubljana,Slovenia,46°04'N,14°33'E,Europe/Ljubljana
Lome,Togo,06°09'N,01°20'E,Africa/Lome
London,England,51°36'N,00°05'W,Europe/London
Luanda,Angola,08°50'S,13°15'E,Africa/Luanda
Lusaka,Zambia,15°28'S,28°16'E,Africa/Lusaka
Luxembourg,Luxembourg,49°37'N,06°09'E,Europe/Luxembourg
Macau,Macao,22°12'N,113°33'E,Asia/Macau
Madinah,Saudi Arabia,24°28'N,39°36'E,Asia/Riyadh
Madrid,Spain,40°25'N,03°45'W,Europe/Madrid
Makkah,Saudi Arabia,21°26'N,39°49'E,Asia/Riyadh
Malabo,Equatorial Guinea,03°45'N,08°50'E,Africa/Malabo
Male,Maldives,04°00'N,73°28'E,Indian/Maldives
Mamoudzou,Mayotte,12°48'S,45°14'E,Indian/Mayotte
Managua,Nicaragua,12°06'N,86°20'W,America/Managua
Manama,Bahrain,26°10'N,50°30'E,Asia/Bahrain
Manila,Philippines,14°40'N,121°03'E,Asia/Manila
Maputo,Mozambique,25°58'S,32°32'E,Africa/Maputo
Maseru,Lesotho,29°18'S,27°30'E,Africa/Maseru
Masqat,Oman,23°37'N,58°36'E,Asia/Muscat
Mbabane,Swaziland,26°18'S,31°06'E,Africa/Mbabane
Mecca,Saudi Arabia,21°26'N,39°49'E,Asia/Riyadh
Medina,Saudi Arabia,24°28'N,39°36'E,Asia/Riyadh
Mexico,Mexico,19°20'N,99°10'W,America/Mexico_City
Minsk,Belarus,53°52'N,27°30'E,Europe/Minsk
Mogadishu,Somalia,02°02'N,45°25'E,Africa/Mogadishu
Monrovia,Liberia,06°18'N,10°47'W,Africa/Monrovia
Montevideo,Uruguay,34°50'S,56°11'W,America/Montevideo
Moroni,Comoros,11°40'S,43°16'E,Indian/Comoro
Moscow,Russian Federation,55°45'N,37°35'E,Europe/Moscow
Moskva,Russian Federation,55°45'N,37°35'E,Europe/Moscow
N'Djamena,Chad,12°10'N,14°59'E,Africa/Ndjamena
Nairobi,Kenya,01°17'S,36°48'E,Africa/Nairobi
Nassau,Bahamas,25°05'N,77°20'W,America/Nassau
New Delhi,India,28°37'N,77°13'E,Asia/Calcutta
Niamey,Niger,13°27'N,02°06'E,Africa/Niamey
Nicosia,Cyprus,35°10'N,33°25'E,Asia/Nicosia
Nouakchott,Mauritania,20°10'S,57°30'E,Africa/Nouakchott
Noumea,New Caledonia,22°17'S,166°30'E,Pacific/Noumea
Nuku'alofa,Tonga,21°10'S,174°00'W,Pacific/Tongatapu
Nuuk,Greenland,64°10'N,51°35'W,America/Godthab
Oranjestad,Aruba,12°32'N,70°02'W,America/Aruba
Oslo,Norway,59°55'N,10°45'E,Europe/Oslo
Ottawa,Canada,45°27'N,75°42'W,US/Eastern
Ouagadougou,Burkina Faso,12°15'N,01°30'W,Africa/Ouagadougou
P'yongyang,Democratic People's Republic of Korea,39°09'N,125°30'E,Asia/Pyongyang
Pago Pago,American Samoa,14°16'S,170°43'W,Pacific/Pago_Pago
Palikir,Micronesia,06°55'N,158°09'E,Pacific/Ponape
Panama,Panama,09°00'N,79°25'W,America/Panama
Papeete,French Polynesia,17°32'S,149°34'W,Pacific/Tahiti
Paramaribo,Suriname,05°50'N,55°10'W,America/Paramaribo
Paris,France,48°50'N,02°20'E,Europe/Paris
Perth,Australia,31°56'S,115°50'E,Australia/Perth
Phnom Penh,Cambodia,11°33'N,104°55'E,Asia/Phnom_Penh
Port Moresby,Papua New Guinea,09°24'S,147°08'E,Pacific/Port_Moresby
Port-Vila,Vanuatu,17°45'S,168°18'E,Pacific/Efate
Port-au-Prince,Haiti,18°40'N,72°20'W,America/Port-au-Prince
Porto-Novo,Benin,06°23'N,02°42'E,Africa/Porto-Novo
Prague,Czech Republic,50°05'N,14°22'E,Europe/Prague
Praia,Cape Verde,15°02'N,23°34'W,Atlantic/Cape_Verde
Pretoria,South Africa,25°44'S,28°12'E,Africa/Johannesburg
Quito,Ecuador,00°15'S,78°35'W,America/Guayaquil
Reykjavik,Iceland,64°10'N,21°57'W,Atlantic/Reykjavik
Riga,Latvia,56°53'N,24°08'E,Europe/Riga
Riyadh,Saudi Arabia,24°41'N,46°42'E,Asia/Riyadh
Road Town,British Virgin Islands,18°27'N,64°37'W,America/Virgin
Rome,Italy,41°54'N,12°29'E,Europe/Rome
Roseau,Dominica,15°20'N,61°24'W,America/Dominica
Saint Pierre,Saint Pierre and Miquelon,46°46'N,56°12'W,America/Miquelon
Saipan,Northern Mariana Islands,15°12'N,145°45'E,Pacific/Saipan
San Jose,Costa Rica,09°55'N,84°02'W,America/Costa_Rica
San Juan,Puerto Rico,18°28'N,66°07'W,America/Puerto_Rico
San Marino,San Marino,43°55'N,12°30'E,Europe/San_Marino
San Salvador,El Salvador,13°40'N,89°10'W,America/El_Salvador
Santiago,Chile,33°24'S,70°40'W,America/Santiago
Santo Domingo,Dominica Republic,18°30'N,69°59'W,America/Santo_Domingo
Sao Tome,Sao Tome and Principe,00°10'N,06°39'E,Africa/Sao_Tome
Sarajevo,Bosnia and Herzegovina,43°52'N,18°26'E,Europe/Sarajevo
Seoul,Republic of Korea,37°31'N,126°58'E,Asia/Seoul
Skopje,The Former Yugoslav Republic of Macedonia,42°01'N,21°26'E,Europe/Skopje
Sofia,Bulgaria,42°45'N,23°20'E,Europe/Sofia
St. Peter Port,Guernsey,49°26'N,02°33'W,Europe/Guernsey
Stanley,Falkland Islands,51°40'S,59°51'W,Atlantic/Stanley
Stockholm,Sweden,59°20'N,18°03'E,Europe/Stockholm
Sucre,Bolivia,16°20'S,68°10'W,America/La_Paz
Suva,Fiji,18°06'S,178°30'E,Pacific/Fiji
Sydney,Australia,33°53'S,151°13'E,Australia/Sydney
T'bilisi,Georgia,41°43'N,44°50'E,Asia/Tbilisi
Tallinn,Estonia,59°22'N,24°48'E,Europe/Tallinn
Tarawa,Kiribati,01°30'N,173°00'E,Pacific/Tarawa
Tashkent,Uzbekistan,41°20'N,69°10'E,Asia/Tashkent
Tegucigalpa,Honduras,14°05'N,87°14'W,America/Tegucigalpa
Tehran,Iran,35°44'N,51°30'E,Asia/Tehran
Thimphu,Bhutan,27°31'N,89°45'E,Asia/Thimphu
Tirane,Albania,41°18'N,19°49'E,Europe/Tirane
Torshavn,Faroe Islands,62°05'N,06°56'W,Atlantic/Faroe
Tripoli,Libyan Arab Jamahiriya,32°49'N,13°07'E,Africa/Tripoli
Tunis,Tunisia,36°50'N,10°11'E,Africa/Tunis
Vaduz,Liechtenstein,47°08'N,09°31'E,Europe/Vaduz
Valletta,Malta,35°54'N,14°31'E,Europe/Malta
Vienna,Austria,48°12'N,16°22'E,Europe/Vienna
Vientiane,Lao People's Democratic Republic,17°58'N,102°36'E,Asia/Vientiane
Vilnius,Lithuania,54°38'N,25°19'E,Europe/Vilnius
W. Indies,Antigua and Barbuda,17°20'N,61°48'W,America/Antigua
Warsaw,Poland,52°13'N,21°00'E,Europe/Warsaw
Washington DC,United States of America,39°91'N,77°02'W,US/Eastern
Wellington,New Zealand,41°19'S,174°46'E,Pacific/Auckland
Willemstad,Netherlands Antilles,12°05'N,69°00'W,America/Curacao
Windhoek,Namibia,22°35'S,17°04'E,Africa/Windhoek
Yamoussoukro,Cote d'Ivoire,06°49'N,05°17'W,Africa/Abidjan
Yangon,Myanmar,16°45'N,96°20'E,Asia/Rangoon
Yaounde,Cameroon,03°50'N,11°35'E,Africa/Douala
Yerevan,Armenia,40°10'N,44°31'E,Asia/Yerevan
Zagreb,Croatia,45°50'N,15°58'E,Europe/Zagreb

# UK Cities
Aberdeen,Scotland,57°08'N,02°06'W,Europe/London
Birmingham,England,52°30'N,01°50'W,Europe/London
Bolton,England,53°35'N,02°15'W,Europe/London
Bradford,England,53°47'N,01°45'W,Europe/London
Bristol,England,51°28'N,02°35'W,Europe/London
Cardiff,Wales,51°29'N,03°13'W,Europe/London
Crawley,England,51°8'N,00°10'W,Europe/London
Edinburgh,Scotland,55°57'N,03°13'W,Europe/London
Glasgow,Scotland,55°50'N,04°15'W,Europe/London
Greenwich,England,51°28'N,00°00'W,Europe/London
Leeds,England,53°48'N,01°35'W,Europe/London
Leicester,England,52°38'N,01°08'W,Europe/London
Liverpool,England,53°25'N,03°00'W,Europe/London
Manchester,England,53°30'N,02°15'W,Europe/London
Newcastle Upon Time,England,54°59'N,01°36'W,Europe/London
Newcastle,England,54°59'N,01°36'W,Europe/London
Norwich,England,52°38'N,01°18'E,Europe/London
Oxford,England,51°45'N,01°15'W,Europe/London
Plymouth,England,50°25'N,04°15'W,Europe/London
Portsmouth,England,50°48'N,01°05'W,Europe/London
Reading,England,	51°27'N,0°58'W,Europe/London
Sheffield,England,53°23'N,01°28'W,Europe/London
Southampton,England,50°55'N,01°25'W,Europe/London
Swansea,England,51°37'N,03°57'W,Europe/London
Swindon,England,51°34'N,01°47'W,Europe/London
Wolverhampton,England,52°35'N,2°08'W,Europe/London
"""

class AstralError(Exception):
    pass

class City(object):
    """Provides access to information for single city."""
    
    def __init__(self, info=None):
        """Initializes the object with a tuple of information.
        
        The tuple should contain items in the following order
        
        ================ =============
        Field            Default
        ================ =============
        name             Greenwich
        country          England
        latitude         51.168
        longitude        0
        time zone name   Europe/London
        ================ =============
            
        See :attr:`timezone` property for a method of obtaining time zone names
        """
        
        self._astral = None
        if info is None:
            self._name = 'Greenwich'
            self._country = 'England'
            self._latitude = 51.168
            self._longitude = 0
            self.timezone = 'Europe/London'
        else:
            try:
                self._name = str(info[0])
                self._country = str(info[1])
                self.latitude = info[2]
                self.longitude = info[3]
                self.timezone = info[4]
            except:
                pass

    def __repr__(self):
        return '%s/%s, tz=%s' % (self._name, self._country, self._timezone)

    def name():
        doc = """The city name."""
        
        def fget(self):
            return self._name
            
        def fset(self, name):
            self._name = name    
            
        return locals()
            
    name = property(**name())
        
    def country():
        doc = """The country in which the city is located."""
        
        def fget(self):
            return self._country
            
        def fset(self, country):
            self._country = country
            
        return locals()
            
    country = property(**country())
        
    def latitude():
        doc = """The city's latitude

        ``latitude`` can be set either as a string or as a number
        
        For strings they must be of the form::
        
            degrees°minutes'[N|S] e.g. 51°31'N
            
        For numbers, negative numbers signify latitudes to the South.
        """
        
        def fget(self):
            return self._latitude
            
        def fset(self, latitude):
            if isinstance(latitude, basestring):
                (deg, rest) = latitude.split("°", 1)
                (minute, rest) = rest.split("'", 1)

                self._latitude = float(deg) + (float(minute)/60)

                if latitude.endswith("S"):
                    self._latitude = -self._latitude
            else:
                self._latitude = float(latitude)
            
        return locals()
        
    latitude = property(**latitude())
        
    def longitude():
        doc = """The city's longitude.

        ``longitude`` can be set either as a string or as a number
        
        For strings they must be of the form::
        
            degrees°minutes'[E|W] e.g. 51°31'W
            
        For numbers, negative numbers signify longitudes to the East.
        This is opposite to the normal convention of +ve being to the West
        but is required for the calculations.
        """
        
        def fget(self):
            return self._longitude
            
        def fset(self, longitude):
            if isinstance(longitude, basestring):
                (deg, rest) = longitude.split("°", 1)
                (minute, rest) = rest.split("'", 1)

                self._longitude = float(deg) + (float(minute)/60)

                # Conventionally locations to the west of 0° are negative
                # but the calculation is based on the opposite
                if longitude.endswith("E"):
                    self._longitude = -self._longitude
            else:
                self._longitude = float(longitude)
            
        return locals()
        
    longitude = property(**longitude())
        
    def timezone():
        doc = """The time zone name in which the city is located.
        
        A list of time zone names can be obtained from pytz. For example.
        
        >>> from pytz import all_timezones
        >>> for tz in all_timezones:
        ...     print tz
        """
        
        def fget(self):
            return self._timezone
        
        def fset(self, name):
            self._timezone = name

        return locals()
            
    timezone = property(**timezone())

    def tz():
        doc = """The timezone."""
        
        def fget(self):
            return pytz.timezone(self._timezone)
            
        return locals()
            
    tz = property(**tz())

    def dawn(self, date=None, local=True):
        """Return dawn time.
        
        Calculates the time in the morning when the sun is a certain number of
        degrees below the horizon. By default this is 6 degrees but can be changed
        by setting the :attr:`Astral.solar_depression` property.
        
        Parameters::
        
            date  - The date for which to calculate the sunrise time.
                    A value of None uses the current date.

            local - True  = Time to be returned in cities time zone (Default);
                    False = Time to be returned in UTC.
        """

        if self._astral is None:
            self._astral = Astral()

        if date is None:
            date = datetime.date.today()

        dawn = self._astral.dawn_utc(date, self.latitude, self.longitude)

        if local:
            return dawn.astimezone(self.tz)            
        else:
            return dawn
        
    def sunrise(self, date=None, local=True):
        """Return sunrise time.
        
        Calculates the time in the morning when the sun is a 0.833 degrees
        below the horizon. This is to account for refraction.
        
        Parameters::

            date  - The date for which to calculate the sunrise time.
                    A value of None uses the current date.

            local - True  = Time to be returned in cities time zone (Default);
                    False = Time to be returned in UTC.
        """

        if self._astral is None:
            self._astral = Astral()
        
        if date is None:
            date = datetime.date.today()

        sunrise = self._astral.sunrise_utc(date, self.latitude, self.longitude)

        if local:
            return sunrise.astimezone(self.tz)            
        else:
            return sunrise
        
    def solar_noon(self, date=None, local=True):
        """Return the solar noon time.
        
        Calculates the time when the sun is at its highest point.
        
        Parameters::
        
            date  - The date for which to calculate the noon time.
                    A value of None uses the current date.
            
            local - True  = Time to be returned in cities time zone (Default);
                    False = Time to be returned in UTC.
        """
        
        if self._astral is None:
            self._astral = Astral()

        if date is None:
            date = datetime.date.today()

        noon = self._astral.solar_noon_utc(date, self.longitude)

        if local:
            return noon.astimezone(self.tz)            
        else:
            return noon
        
    def sunset(self, date=None, local=True):
        """Return sunset time.
        
        Calculates the time in the evening when the sun is a 0.833 degrees
        below the horizon. This is to account for refraction.
        
        Parameters::
        
            date  - The date for which to calculate the sunset time.
                    A value of None uses the current date.
            
            local - True  = Time to be returned in cities time zone (Default);
                    False = Time to be returned in UTC.
        """
        
        if self._astral is None:
            self._astral = Astral()

        if date is None:
            date = datetime.date.today()

        sunset = self._astral.sunset_utc(date, self.latitude, self.longitude)

        if local:
            return sunset.astimezone(self.tz)            
        else:
            return sunset
        
    def dusk(self, date=None, local=True):
        """Return dusk time.
        
        Calculates the time in the evening when the sun is a certain number of
        degrees below the horizon. By default this is 6 degrees but can be changed
        by setting the :attr:`Astral.solar_depression` property.
        
        Parameters::
        
            date  - The date for which to calculate the dusk time.
                    A value of None uses the current date.
            
            local - True  = Time to be returned in cities time zone (Default);
                    False = Time to be returned in UTC.
        """
        
        if self._astral is None:
            self._astral = Astral()

        if date is None:
            date = datetime.date.today()

        dusk = self._astral.dusk_utc(date, self.latitude, self.longitude)

        if local:
            return dusk.astimezone(self.tz)            
        else:
            return dusk
    
    def sun(self, date=None, local=True):
        """Returns dawn, sunrise, noon, sunset and dusk as a dictionary.
        
        Parameters::
        
            date  - The date for which to calculate the times.
                    A value of None uses the current date.
            
            local - True  = Time to be returned in cities time zone (Default);
                    False = Time to be returned in UTC.
        """
        
        if self._astral is None:
            self._astral = Astral()

        if date is None:
            date = datetime.date.today()

        sun = self._astral.sun_utc(date, self.latitude, self.longitude)

        if local:
            for key, dt in sun.items():
                sun[key] = dt.astimezone(self.tz)

        return sun

    def rahukaalam(self, date=None, local=True):
        """Calculates the period of rahukaalam.
        
        Parameters::
        
            date  - The date for which to calculate rahukaalam period.
                    A value of None uses the current date.
            
            local - True  = Time to be returned in cities time zone (Default);
                    False = Time to be returned in UTC.
        """

        if self._astral is None:
            self._astral = Astral()

        if date is None:
            date = datetime.date.today()

        rahukaalam = self._astral.rahukaalam_utc(date, self.latitude, self.longitude)

        if local:
            for key, dt in rahukaalam.items():
                rahukaalam[key] = dt.astimezone(self.tz)
            
        return rahukaalam
    
    def solar_azimuth(self, dateandtime=None):
        """Calculates the solar azimuth angle for a specific time.
        
        The angle returned is in degrees clockwise from North.
        
        Parameters::
        
            dateandtime - The date and time for which to calculate the angle.
        """

        if self._astral is None:
            self._astral = Astral()

        if dateandtime is None:
            dateandtime = datetime.datetime.now(tz=self.tz)
            
        return self._astral.solar_azimuth(dateandtime, self.latitude, self.longitude)
    
    def solar_elevation(self, dateandtime=None):
        """Calculates the solar elevation angle for a specific time.
        
        The angle returned is in degrees from the horizon
        
        Parameters::
        
            dateandtime - The date and time for which to calculate the angle.
        """

        if self._astral is None:
            self._astral = Astral()

        if dateandtime is None:
            dateandtime = datetime.datetime.now(tz=self.tz)

        return self._astral.solar_elevation(dateandtime, self.latitude, self.longitude)
        
    def astral():
        def fget(self):
            return self._astral
            
        def fset(self, astral):
            self._astral = astral
            
        return locals()
        
    astral = property(**astral())
    

class Astral(object):
    def __init__(self):
        """Initialise the list of cities.
        """
        
        self._cities = {}
        self._init_cities()
        
        self._depression = 6  # Set default depression in degrees

    def __getitem__(self, value):
        """Returns a City object for the specified city.
        
        Handles city names with spaces and mixed case.
        """

        city_name = str(value).lower().replace(' ', '_')

        if city_name[0] == "'" and city_name[-1] == "'":
            city_name = city_name.strip("'")

        if city_name[0] == '"' and city_name[-1] == '"':
            city_name = city_name.strip('"')
            
        city_name = city_name.strip()

        for (name, city) in self._cities.items():
            if name.lower().replace(' ', '_') == city_name:
                return city

        raise KeyError('Unrecognised city name - %s' % value)

    def cities():
        doc = """Returns a dictionary of cities indexed by city name.
        """

        def fget(self):
            return self._cities
            
        return locals()
        
    cities = property(**cities())

    def solar_depression():
        doc = """The number of degrees the sun must be below the horizon for the dawn/dusk calc.
        
        Can either be set as a number of degrees below the horizon or as
        one of the following strings
        
        ============= =======
        String        Degrees
        ============= =======
        civil            6.0
        nautical        12.0
        astronomical    18.0
        ============= =======
        """
        
        def fget(self):
            return self._depression
            
        def fset(self, depression):
            if isinstance(depression, basestring):
                try:
                    self._depression = {'civil': 6, 'nautical': 12, 'astronomical': 18}[depression]
                except:
                    raise KeyError("solar_depression must be either a number or one of 'civil', 'nautical' or 'astronomical'")
            else:
                self._depression = float(depression)
            
        return locals()
        
    solar_depression = property(**solar_depression())

    def sun_utc(self, date, latitude, longitude):
        """Returns dawn, sunrise, noon, sunset and dusk times as a dictionary.
        """
        
        dawn = self.dawn_utc(date, latitude, longitude)
        sunrise = self.sunrise_utc(date, latitude, longitude)
        noon = self.solar_noon_utc(date, longitude)
        sunset = self.sunset_utc(date, latitude, longitude)
        dusk = self.dusk_utc(date, latitude, longitude)
        
        return {'dawn': dawn, 'sunrise': sunrise, 'noon': noon, 'sunset': sunset, 'dusk': dusk}

    def dawn_utc(self, date, latitude, longitude):
        """Calculate dawn time for a specific date at a particular position.
        
        Returns date/time in UTC
        """
        
        julianday = self._julianday(date.day, date.month, date.year)

        if latitude > 89.8:
            latitude = 89.8
            
        if latitude < -89.8:
            latitude = -89.8
        
        t = self._jday_to_jcentury(julianday)
        eqtime = self._eq_of_time(t)
        solarDec = self._sun_declination(t)
        
        try:
            hourangle = self._hour_angle_sunrise(latitude, solarDec)
        except:
            raise AstralError('Sun remains below horizon on this day, at this location.')

        delta = longitude - degrees(hourangle)
        timeDiff = 4.0 * delta
        timeUTC = 720.0 + timeDiff - eqtime

        newt = self._jday_to_jcentury(self._jcentury_to_jday(t) + timeUTC / 1440.0)
        eqtime = self._eq_of_time(newt)
        solarDec = self._sun_declination(newt)
        hourangle = self._hour_angle_dawn(latitude, solarDec, self._depression)
        delta = longitude - degrees(hourangle)
        timeDiff = 4 * delta
        timeUTC = 720 + timeDiff - eqtime
        
        timeUTC = timeUTC/60.0
        hour = int(timeUTC)
        minute = int((timeUTC - hour) * 60)
        second = int((((timeUTC - hour) * 60) - minute) * 60)

        if hour > 23.0:
            hour -= 24
            date += datetime.timedelta(days=1)

        dawn = datetime.datetime(date.year, date.month, date.day, hour, minute, second, tzinfo=pytz.utc)

        return dawn

    def sunrise_utc(self, date, latitude, longitude):
        """Calculate sunrise time for a specific date at a particular position.
        
        Returns date/time in UTC
        """
        
        julianday = self._julianday(date.day, date.month, date.year)

        t = self._jday_to_jcentury(julianday)
        eqtime = self._eq_of_time(t)
        solarDec = self._sun_declination(t)

        try:
            hourangle = self._hour_angle_sunrise(latitude, solarDec)
        except:
            raise AstralError('Sun remains below horizon on this day, at this location.')

        delta = longitude - degrees(hourangle)
        timeDiff = 4.0 * delta
        timeUTC = 720.0 + timeDiff - eqtime

        newt = self._jday_to_jcentury(self._jcentury_to_jday(t) + timeUTC / 1440.0)
        eqtime = self._eq_of_time(newt)
        solarDec = self._sun_declination(newt)
        hourangle = self._hour_angle_sunrise(latitude, solarDec)
        delta = longitude - degrees(hourangle)
        timeDiff = 4 * delta
        timeUTC = 720 + timeDiff - eqtime
        
        timeUTC = timeUTC/60.0
        hour = int(timeUTC)
        minute = int((timeUTC - hour) * 60)
        second = int((((timeUTC - hour) * 60) - minute) * 60)

        if hour > 23:
            hour -= 24
            date += datetime.timedelta(days=1)

        sunrise = datetime.datetime(date.year, date.month, date.day, hour, minute, second, tzinfo=pytz.utc)

        return sunrise

    def solar_noon_utc(self, date, longitude):
        """Calculate solar noon time for a specific date at a particular position.
        
        Returns date/time in UTC
        """
        
        julianday = self._julianday(date.day, date.month, date.year)

        newt = self._jday_to_jcentury(julianday + 0.5 + longitude / 360.0)

        eqtime = self._eq_of_time(newt)
        solarNoonDec = self._sun_declination(newt)
        timeUTC = 720.0 + (longitude * 4.0) - eqtime

        timeUTC = timeUTC/60.0
        hour = int(timeUTC)
        minute = int((timeUTC - hour) * 60)
        second = int((((timeUTC - hour) * 60) - minute) * 60)

        if hour > 23:
            hour -= 24
            date += datetime.timedelta(days=1)

        noon = datetime.datetime(date.year, date.month, date.day, hour, minute, second, tzinfo=pytz.utc)

        return noon

    def sunset_utc(self, date, latitude, longitude):
        """Calculate sunset time for a specific date at a particular position.
        
        Returns date/time in UTC
        """
        
        julianday = self._julianday(date.day, date.month, date.year)

        t = self._jday_to_jcentury(julianday)
        eqtime = self._eq_of_time(t)
        solarDec = self._sun_declination(t)

        try:
            hourangle = self._hour_angle_sunset(latitude, solarDec)
        except:
            raise AstralError('Sun remains below horizon on this day, at this location.')

        delta = longitude - degrees(hourangle)
        timeDiff = 4.0 * delta
        timeUTC = 720.0 + timeDiff - eqtime

        newt = self._jday_to_jcentury(self._jcentury_to_jday(t) + timeUTC / 1440.0)
        eqtime = self._eq_of_time(newt)
        solarDec = self._sun_declination(newt)
        hourangle = self._hour_angle_sunset(latitude, solarDec)
        delta = longitude - degrees(hourangle)
        timeDiff = 4 * delta
        timeUTC = 720 + timeDiff - eqtime
        
        timeUTC = timeUTC/60.0
        hour = int(timeUTC)
        minute = int((timeUTC - hour) * 60)
        second = int((((timeUTC - hour) * 60) - minute) * 60)

        if hour > 23:
            hour -= 24
            date += datetime.timedelta(days=1)

        sunset = datetime.datetime(date.year, date.month, date.day, hour, minute, second, tzinfo=pytz.utc)

        return sunset

    def dusk_utc(self, date, latitude, longitude):
        """Calculate dusk time for a specific date at a particular position.
        
        Returns date/time in UTC
        """
        
        julianday = self._julianday(date.day, date.month, date.year)

        if latitude > 89.8:
            latitude = 89.8
            
        if latitude < -89.8:
            latitude = -89.8
        
        t = self._jday_to_jcentury(julianday)
        eqtime = self._eq_of_time(t)
        solarDec = self._sun_declination(t)

        try:
            hourangle = self._hour_angle_sunset(latitude, solarDec)
        except:
            raise AstralError('Sun remains below horizon on this day, at this location.')

        delta = longitude - degrees(hourangle)
        timeDiff = 4.0 * delta
        timeUTC = 720.0 + timeDiff - eqtime

        newt = self._jday_to_jcentury(self._jcentury_to_jday(t) + timeUTC / 1440.0)
        eqtime = self._eq_of_time(newt)
        solarDec = self._sun_declination(newt)
        hourangle = self._hour_angle_dusk(latitude, solarDec, self._depression)
        delta = longitude - degrees(hourangle)
        timeDiff = 4 * delta
        timeUTC = 720 + timeDiff - eqtime
        
        timeUTC = timeUTC/60.0
        hour = int(timeUTC)
        minute = int((timeUTC - hour) * 60)
        second = int((((timeUTC - hour) * 60) - minute) * 60)

        if hour > 23:
            hour -= 24
            date += datetime.timedelta(days=1)

        dusk = datetime.datetime(date.year, date.month, date.day, hour, minute, second, tzinfo=pytz.utc)

        return dusk

    def rahukaalam_utc(self, date, latitude, longitude):
        """Calculate ruhakaalam times at a particular location.
        """
        
        if date is None:
            date = datetime.date.today()

        try:
            sunrise = self.sunrise_utc(date, latitude, longitude)
            sunset = self.sunset_utc(date, latitude, longitude)
        except:
            raise AstralError('Sun remains below horizon on this day, at this location.')
        
        octant_duration = (sunset - sunrise) / 8

        # Mo,Sa,Fr,We,Th,Tu,Su
        octant_index = [1,6,4,5,3,2,7]
        
        weekday = date.weekday()
        octant = octant_index[weekday]
        
        start = sunrise + (octant_duration * octant)
        end = start + octant_duration
        
        return {'start': start, 'end': end}

    def solar_azimuth(self, dateandtime, latitude, longitude):
        """Calculate the azimuth of the sun as a specific date/time and location.
        """
    
        if latitude > 89.8:
            latitude = 89.8
            
        if latitude < -89.8:
            latitude = -89.8
    
        zone = -dateandtime.utcoffset().seconds / 3600.0
        utc_datetime = dateandtime.astimezone(pytz.utc)
        timenow = utc_datetime.hour + (utc_datetime.minute / 60.0) + (utc_datetime.second / 3600)

        JD = self._julianday(dateandtime.day, dateandtime.month, dateandtime.year)
        t = self._jday_to_jcentury(JD + timenow / 24.0)
        R = self._sun_rad_vector(t)
        alpha = self._sun_rt_ascension(t)
        theta = self._sun_declination(t)
        Etime = self._eq_of_time(t)
    
        eqtime = Etime
        solarDec = theta   # in degrees
        earthRadVec = R
    
        solarTimeFix = eqtime - (4.0 * longitude) + (60 * zone)
        trueSolarTime = dateandtime.hour * 60.0 + dateandtime.minute + dateandtime.second / 60.0 + solarTimeFix
        #    in minutes
    
        while trueSolarTime > 1440:
            trueSolarTime = trueSolarTime - 1440
        
        hourangle = trueSolarTime / 4.0 - 180.0
        #    Thanks to Louis Schwarzmayr for the next line:
        if hourangle < -180:
            hourangle = hourangle + 360.0
    
        harad = radians(hourangle)
    
        csz = sin(radians(latitude)) * sin(radians(solarDec)) + \
              cos(radians(latitude)) * cos(radians(solarDec)) * cos(harad)
    
        if csz > 1.0:
            csz = 1.0
        elif csz < -1.0:
            csz = -1.0
        
        zenith = degrees(acos(csz))
    
        azDenom = (cos(radians(latitude)) * sin(radians(zenith)))
        
        if (abs(azDenom) > 0.001):
            azRad = ((sin(radians(latitude)) *  cos(radians(zenith))) - sin(radians(solarDec))) / azDenom
            
            if abs(azRad) > 1.0:
                if azRad < 0:
                    azRad = -1.0
                else:
                    azRad = 1.0
    
            azimuth = 180.0 - degrees(acos(azRad))
    
            if hourangle > 0.0:
                azimuth = -azimuth
        else:
            if latitude > 0.0:
                azimuth = 180.0
            else:
                azimuth = 0#
    
        if azimuth < 0.0:
            azimuth = azimuth + 360.0
                 
        return azimuth

    def solar_elevation(self, dateandtime, latitude, longitude):
        """Calculate the elevation of the sun as a specific date/time and location.
        """
    
        if latitude > 89.8:
            latitude = 89.8
            
        if latitude < -89.8:
            latitude = -89.8

        zone = -dateandtime.utcoffset().seconds / 3600.0
        utc_datetime = dateandtime.astimezone(pytz.utc)
        timenow = utc_datetime.hour + (utc_datetime.minute / 60.0) + (utc_datetime.second / 3600)
    
        JD = self._julianday(dateandtime.day, dateandtime.month, dateandtime.year)
        t = self._jday_to_jcentury(JD + timenow / 24.0)
        R = self._sun_rad_vector(t)
        alpha = self._sun_rt_ascension(t)
        theta = self._sun_declination(t)
        Etime = self._eq_of_time(t)
    
        eqtime = Etime
        solarDec = theta   # in degrees
        earthRadVec = R
    
        solarTimeFix = eqtime - (4.0 * longitude) + (60 * zone)
        trueSolarTime = dateandtime.hour * 60.0 + dateandtime.minute + dateandtime.second / 60.0 + solarTimeFix
        #    in minutes
    
        while trueSolarTime > 1440:
            trueSolarTime = trueSolarTime - 1440
        
        hourangle = trueSolarTime / 4.0 - 180.0
        #    Thanks to Louis Schwarzmayr for the next line:
        if hourangle < -180:
            hourangle = hourangle + 360.0
    
        harad = radians(hourangle)
    
        csz = sin(radians(latitude)) * sin(radians(solarDec)) + \
              cos(radians(latitude)) * cos(radians(solarDec)) * cos(harad)
    
        if csz > 1.0:
            csz = 1.0
        elif csz < -1.0:
            csz = -1.0
        
        zenith = degrees(acos(csz))
    
        azDenom = (cos(radians(latitude)) * sin(radians(zenith)))
        
        if (abs(azDenom) > 0.001):
            azRad = ((sin(radians(latitude)) *  cos(radians(zenith))) - sin(radians(solarDec))) / azDenom
            
            if abs(azRad) > 1.0:
                if azRad < 0:
                    azRad = -1.0
                else:
                    azRad = 1.0
    
            azimuth = 180.0 - degrees(acos(azRad))
    
            if hourangle > 0.0:
                azimuth = -azimuth
        else:
            if latitude > 0.0:
                azimuth = 180.0
            else:
                azimuth = 0#
    
        if azimuth < 0.0:
            azimuth = azimuth + 360.0
                    
        exoatmElevation = 90.0 - zenith

        if exoatmElevation > 85.0:
            refractionCorrection = 0.0
        else:
            te = tan(radians(exoatmElevation))
            if exoatmElevation > 5.0:
                refractionCorrection = 58.1 / te - 0.07 / (te * te * te) + 0.000086 / (te * te * te * te * te)
            elif exoatmElevation > -0.575:
                step1 = (-12.79 + exoatmElevation * 0.711)
                step2 = (103.4 + exoatmElevation * (step1))
                step3 = (-518.2 + exoatmElevation * (step2))
                refractionCorrection = 1735.0 + exoatmElevation * (step3)
            else:
                refractionCorrection = -20.774 / te
    
            refractionCorrection = refractionCorrection / 3600.0
            
        solarzen = zenith - refractionCorrection
                     
        solarelevation = 90.0 - solarzen
    
        return solarelevation

    def _julianday(self, day, month, year):
        if month <= 2:
            year = year - 1
            month = month + 12
        
        A = floor(year / 100.0)
        B = 2 - A + floor(A / 4.0)

        return floor(365.25 * (year + 4716)) + floor(30.6001 * (month + 1)) + day + B - 1524.5
        
    def _jday_to_jcentury(self, julianday):
        return (julianday - 2451545.0) / 36525.0

    def _jcentury_to_jday(self, juliancentury):
        return (juliancentury * 36525.0) + 2451545.0

    def _mean_obliquity_of_ecliptic(self, juliancentury):
        seconds = 21.448 - juliancentury * (46.815 + juliancentury * (0.00059 - juliancentury * (0.001813)))
        return 23.0 + (26.0 + (seconds / 60.0)) / 60.0

    def _obliquity_correction(self, juliancentury):
        e0 = self._mean_obliquity_of_ecliptic(juliancentury)

        omega = 125.04 - 1934.136 * juliancentury
        return e0 + 0.00256 * cos(radians(omega))
    
    def _geom_mean_long_sun(self, juliancentury):
        l0 = 280.46646 + juliancentury * (36000.76983 + 0.0003032 * juliancentury)
        return l0 % 360.0
        
    def _eccentricity_earth_orbit(self, juliancentury):
        return 0.016708634 - juliancentury * (0.000042037 + 0.0000001267 * juliancentury)
        
    def _geom_mean_anomaly_sun(self, juliancentury):
        return 357.52911 + juliancentury * (35999.05029 - 0.0001537 * juliancentury)

    def _eq_of_time(self, juliancentury):
        epsilon = self._obliquity_correction(juliancentury)
        l0 = self._geom_mean_long_sun(juliancentury)
        e = self._eccentricity_earth_orbit(juliancentury)
        m = self._geom_mean_anomaly_sun(juliancentury)

        y = tan(radians(epsilon) / 2.0)
        y = y * y

        sin2l0 = sin(2.0 * radians(l0))
        sinm = sin(radians(m))
        cos2l0 = cos(2.0 * radians(l0))
        sin4l0 = sin(4.0 * radians(l0))
        sin2m = sin(2.0 * radians(m))

        Etime = y * sin2l0 - 2.0 * e * sinm + 4.0 * e * y * sinm * cos2l0 - \
                0.5 * y * y * sin4l0 - 1.25 * e * e * sin2m

        return degrees(Etime) * 4.0

    def _sun_eq_of_center(self, juliancentury):
        m = self._geom_mean_anomaly_sun(juliancentury)

        mrad = radians(m)
        sinm = sin(mrad)
        sin2m = sin(mrad + mrad)
        sin3m = sin(mrad + mrad + mrad)

        c = sinm * (1.914602 - juliancentury * (0.004817 + 0.000014 * juliancentury)) + \
            sin2m * (0.019993 - 0.000101 * juliancentury) + sin3m * 0.000289
            
        return c

    def _sun_true_long(self, juliancentury):
        l0 = self._geom_mean_long_sun(juliancentury)
        c = self._sun_eq_of_center(juliancentury)

        return l0 + c

    def _sun_apparent_long(self, juliancentury):
        O = self._sun_true_long(juliancentury)

        omega = 125.04 - 1934.136 * juliancentury
        return O - 0.00569 - 0.00478 * sin(radians(omega))

    def _sun_declination(self, juliancentury):
        e = self._obliquity_correction(juliancentury)
        lambd = self._sun_apparent_long(juliancentury)

        sint = sin(radians(e)) * sin(radians(lambd))
        return degrees(asin(sint))

    def _hour_angle(self, latitude, solar_dec, solar_depression):
        latRad = radians(latitude)
        sdRad = radians(solar_dec)

        HA = (acos(cos(radians(90 + solar_depression)) / (cos(latRad) * cos(sdRad)) - tan(latRad) * tan(sdRad)))
        
        return HA

    def _hour_angle_sunrise(self, latitude, solar_dec):
        return self._hour_angle(latitude, solar_dec, 0.833)
        
    def _hour_angle_sunset(self, latitude, solar_dec):
        return -self._hour_angle(latitude, solar_dec, 0.833)

    def _hour_angle_dawn(self, latitude, solar_dec, solar_depression):
        return self._hour_angle(latitude, solar_dec, solar_depression)

    def _hour_angle_dusk(self, latitude, solar_dec, solar_depression):
        return -self._hour_angle(latitude, solar_dec, solar_depression)

    def _sun_true_anomoly(self, juliancentury):
        m = self._geom_mean_anomaly_sun(juliancentury)
        c = self._sun_eq_of_center(juliancentury)

        return m + c

    def _sun_rad_vector(self, juliancentury):
        v = self._sun_true_anomoly(juliancentury)
        e = self._eccentricity_earth_orbit(juliancentury)
 
        return (1.000001018 * (1 - e * e)) / (1 + e * cos(radians(v)))

    def _sun_rt_ascension(self, juliancentury):
        e = self._obliquity_correction(juliancentury)
        lambd = self._sun_apparent_long(juliancentury)
 
        tananum = (cos(radians(e)) * sin(radians(lambd)))
        tanadenom = (cos(radians(lambd)))

        return degrees(atan2(tananum, tanadenom))

    def _init_cities(self):
        cities = _CITY_INFO.split('\n')
        for line in cities:
            line = line.strip()
            if line != '' and line[0] != '#':
                if line[-1] == '\n':
                    line = line[:-1]
                
                city_info = line.split(',')
                if city_info[0] not in self._cities:
                    city = City(city_info)
                    city.astral = self
                    self._cities[city_info[0]] = city

