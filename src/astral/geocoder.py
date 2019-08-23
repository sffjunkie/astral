"""Astral geocoder is a local database of locations.

To get the location info you can use the lookup function e.g. ::

    from astral.geocoder import lookup
    l = lookup("London")
"""

from functools import reduce
from typing import Dict, List, Tuple, Optional, Union

from astral import LocationInfo, latlng_to_float


__all__ = ["Geocoder", "lookup"]


# region Location Info
# name,region,timezone,latitude,longitude,elevation
_LOCATION_INFO = """Abu Dhabi,UAE,Asia/Dubai,24°28'N,54°22'E,5.0
Abu Dhabi,United Arab Emirates,Asia/Dubai,24°28'N,54°22'E,5.0
Abuja,Nigeria,Africa/Lagos,09°05'N,07°32'E,342.0
Accra,Ghana,Africa/Accra,05°35'N,00°06'W,61.0
Addis Ababa,Ethiopia,Africa/Addis_Ababa,09°02'N,38°42'E,2355.0
Adelaide,Australia,Australia/Adelaide,34°56'S,138°36'E,50.0
Al Jubail,Saudi Arabia,Asia/Riyadh,25°24'N,49°39'W,8.0
Algiers,Algeria,Africa/Algiers,36°42'N,03°08'E,224.0
Amman,Jordan,Asia/Amman,31°57'N,35°52'E,1100.0
Amsterdam,Netherlands,Europe/Amsterdam,52°23'N,04°54'E,2.0
Andorra la Vella,Andorra,Europe/Andorra,42°31'N,01°32'E,1023.0
Ankara,Turkey,Europe/Istanbul,39°57'N,32°54'E,938.0
Antananarivo,Madagascar,Indian/Antananarivo,18°55'S,47°31'E,1276.0
Apia,Samoa,Pacific/Apia,13°50'S,171°50'W,2.0
Ashgabat,Turkmenistan,Asia/Ashgabat,38°00'N,57°50'E,219.0
Asmara,Eritrea,Africa/Asmara,15°19'N,38°55'E,2325.0
Astana,Kazakhstan,Asia/Qyzylorda,51°10'N,71°30'E,347.0
Asuncion,Paraguay,America/Asuncion,25°10'S,57°30'W,124.0
Athens,Greece,Europe/Athens,37°58'N,23°46'E,338.0
Avarua,Cook Islands,Etc/GMT-10,21°12'N,159°46'W,208.0
Baghdad,Iraq,Asia/Baghdad,33°20'N,44°30'E,41.0
Baku,Azerbaijan,Asia/Baku,40°29'N,49°56'E,30.0
Bamako,Mali,Africa/Bamako,12°34'N,07°55'W,350.0
Bandar Seri Begawan,Brunei Darussalam,Asia/Brunei,04°52'N,115°00'E,1.0
Bangkok,Thailand,Asia/Bangkok,13°45'N,100°35'E,2.0
Bangui,Central African Republic,Africa/Bangui,04°23'N,18°35'E,373.0
Banjul,Gambia,Africa/Banjul,13°28'N,16°40'W,5.0
Basse-Terre,Guadeloupe,America/Guadeloupe,16°00'N,61°44'W,1.0
Basseterre,Saint Kitts and Nevis,America/St_Kitts,17°17'N,62°43'W,50.0
Beijing,China,Asia/Harbin,39°55'N,116°20'E,59.0
Beirut,Lebanon,Asia/Beirut,33°53'N,35°31'E,56.0
Belfast,Northern Ireland,Europe/Belfast,54°36'N,5°56'W,9.0
Belgrade,Yugoslavia,Europe/Belgrade,44°50'N,20°37'E,90.0
Belmopan,Belize,America/Belize,17°18'N,88°30'W,63.0
Berlin,Germany,Europe/Berlin,52°30'N,13°25'E,35.0
Bern,Switzerland,Europe/Zurich,46°57'N,07°28'E,510.0
Bishkek,Kyrgyzstan,Asia/Bishkek,42°54'N,74°46'E,772.0
Bissau,Guinea-Bissau,Africa/Bissau,11°45'N,15°45'W,0.0
Bloemfontein,South Africa,Africa/Johannesburg,29°12'S,26°07'E,1398.0
Bogota,Colombia,America/Bogota,04°34'N,74°00'W,2620.0
Brasilia,Brazil,Brazil/East,15°47'S,47°55'W,1087.0
Bratislava,Slovakia,Europe/Bratislava,48°10'N,17°07'E,132.0
Brazzaville,Congo,Africa/Brazzaville,04°09'S,15°12'E,156.0
Bridgetown,Barbados,America/Barbados,13°05'N,59°30'W,1.0
Brisbane,Australia,Australia/Brisbane,27°30'S,153°01'E,25.0
Brussels,Belgium,Europe/Brussels,50°51'N,04°21'E,62.0
Bucharest,Romania,Europe/Bucharest,44°27'N,26°10'E,71.0
Bucuresti,Romania,Europe/Bucharest,44°27'N,26°10'E,71.0
Budapest,Hungary,Europe/Budapest,47°29'N,19°05'E,120.0
Buenos Aires,Argentina,America/Buenos_Aires,34°62'S,58°44'W,6.0
Bujumbura,Burundi,Africa/Bujumbura,03°16'S,29°18'E,782.0
Cairo,Egypt,Africa/Cairo,30°01'N,31°14'E,74.0
Canberra,Australia,Australia/Canberra,35°15'S,149°08'E,575.0
Cape Town,South Africa,Africa/Johannesburg,33°55'S,18°22'E,1700.0
Caracas,Venezuela,America/Caracas,10°30'N,66°55'W,885.0
Castries,Saint Lucia,America/St_Lucia,14°02'N,60°58'W,125.0
Cayenne,French Guiana,America/Cayenne,05°05'N,52°18'W,9.0
Charlotte Amalie,United States of Virgin Islands,America/Virgin,18°21'N,64°56'W,0.0
Chisinau,Moldova,Europe/Chisinau,47°02'N,28°50'E,122.0
Conakry,Guinea,Africa/Conakry,09°29'N,13°49'W,26.0
Copenhagen,Denmark,Europe/Copenhagen,55°41'N,12°34'E,5.0
Cotonou,Benin,Africa/Porto-Novo,06°23'N,02°42'E,5.0
Dakar,Senegal,Africa/Dakar,14°34'N,17°29'W,24.0
Damascus,Syrian Arab Republic,Asia/Damascus,33°30'N,36°18'E,609.0
Dammam,Saudi Arabia,Asia/Riyadh,26°30'N,50°12'E,1.0
Dhaka,Bangladesh,Asia/Dhaka,23°43'N,90°26'E,8.0
Dili,East Timor,Asia/Dili,08°29'S,125°34'E,11.0
Djibouti,Djibouti,Africa/Djibouti,11°08'N,42°20'E,19.0
Dodoma,United Republic of Tanzania,Africa/Dar_es_Salaam,06°08'S,35°45'E,1119.0
Doha,Qatar,Asia/Qatar,25°15'N,51°35'E,10.0
Douglas,Isle Of Man,Europe/London,54°9'N,4°29'W,35.0
Dublin,Ireland,Europe/Dublin,53°21'N,06°15'W,85.0
Dushanbe,Tajikistan,Asia/Dushanbe,38°33'N,68°48'E,803.0
El Aaiun,Morocco,UTC,27°9'N,13°12'W,64.0
Fort-de-France,Martinique,America/Martinique,14°36'N,61°02'W,9.0
Freetown,Sierra Leone,Africa/Freetown,08°30'N,13°17'W,26.0
Funafuti,Tuvalu,Pacific/Funafuti,08°31'S,179°13'E,2.0
Gaborone,Botswana,Africa/Gaborone,24°45'S,25°57'E,1005.0
George Town,Cayman Islands,America/Cayman,19°20'N,81°24'W,3.0
Georgetown,Guyana,America/Guyana,06°50'N,58°12'W,30.0
Gibraltar,Gibraltar,Europe/Gibraltar,36°9'N,5°21'W,3.0
Guatemala,Guatemala,America/Guatemala,14°40'N,90°22'W,1500.0
Hanoi,Viet Nam,Asia/Saigon,21°05'N,105°55'E,6.0
Harare,Zimbabwe,Africa/Harare,17°43'S,31°02'E,1503.0
Havana,Cuba,America/Havana,23°08'N,82°22'W,59.0
Helsinki,Finland,Europe/Helsinki,60°15'N,25°03'E,56.0
Hobart,Tasmania,Australia/Hobart,42°53'S,147°19'E,4.0
Hong Kong,China,Asia/Hong_Kong,22°16'N,114°09'E,8.0
Honiara,Solomon Islands,Pacific/Guadalcanal,09°27'S,159°57'E,8.0
Islamabad,Pakistan,Asia/Karachi,33°40'N,73°10'E,508.0
Jakarta,Indonesia,Asia/Jakarta,06°09'S,106°49'E,6.0
Jerusalem,Israel,Asia/Jerusalem,31°47'N,35°12'E,775.0
Juba,South Sudan,Africa/Juba,4°51'N,31°36'E,550.0
Jubail,Saudi Arabia,Asia/Riyadh,27°02'N,49°39'E,2.0
Kabul,Afghanistan,Asia/Kabul,34°28'N,69°11'E,1791.0
Kampala,Uganda,Africa/Kampala,00°20'N,32°30'E,1155.0
Kathmandu,Nepal,Asia/Kathmandu,27°45'N,85°20'E,1337.0
Khartoum,Sudan,Africa/Khartoum,15°31'N,32°35'E,380.0
Kiev,Ukraine,Europe/Kiev,50°30'N,30°28'E,153.0
Kigali,Rwanda,Africa/Kigali,01°59'S,30°04'E,1497.0
Kingston,Jamaica,America/Jamaica,18°00'N,76°50'W,9.0
Kingston,Norfolk Island,Pacific/Norfolk,45°20'S,168°43'E,113.0
Kingstown,Saint Vincent and the Grenadines,America/St_Vincent,13°10'N,61°10'W,1.0
Kinshasa,Democratic Republic of the Congo,Africa/Kinshasa,04°20'S,15°15'E,312.0
Koror,Palau,Pacific/Palau,07°20'N,134°28'E,33.0
Kuala Lumpur,Malaysia,Asia/Kuala_Lumpur,03°09'N,101°41'E,22.0
Kuwait,Kuwait,Asia/Kuwait,29°30'N,48°00'E,55.0
La Paz,Bolivia,America/La_Paz,16°20'S,68°10'W,4014.0
Libreville,Gabon,Africa/Libreville,00°25'N,09°26'E,15.0
Lilongwe,Malawi,Africa/Blantyre,14°00'S,33°48'E,1229.0
Lima,Peru,America/Lima,12°00'S,77°00'W,13.0
Lisbon,Portugal,Europe/Lisbon,38°42'N,09°10'W,123.0
Ljubljana,Slovenia,Europe/Ljubljana,46°04'N,14°33'E,385.0
Lome,Togo,Africa/Lome,06°09'N,01°20'E,25.0
London,England,Europe/London,51°28'24"N,00°00'3"W,24.0
Luanda,Angola,Africa/Luanda,08°50'S,13°15'E,6.0
Lusaka,Zambia,Africa/Lusaka,15°28'S,28°16'E,1154.0
Luxembourg,Luxembourg,Europe/Luxembourg,49°37'N,06°09'E,232.0
Macau,Macao,Asia/Macau,22°12'N,113°33'E,6.0
Madinah,Saudi Arabia,Asia/Riyadh,24°28'N,39°36'E,631.0
Madrid,Spain,Europe/Madrid,40°25'N,03°45'W,582.0
Majuro,Marshall Islands,Pacific/Majuro,7°4'N,171°16'E,65.0
Makkah,Saudi Arabia,Asia/Riyadh,21°26'N,39°49'E,240.0
Malabo,Equatorial Guinea,Africa/Malabo,03°45'N,08°50'E,56.0
Male,Maldives,Indian/Maldives,04°00'N,73°28'E,2.0
Mamoudzou,Mayotte,Indian/Mayotte,12°48'S,45°14'E,420.0
Managua,Nicaragua,America/Managua,12°06'N,86°20'W,50.0
Manama,Bahrain,Asia/Bahrain,26°10'N,50°30'E,2.0
Manila,Philippines,Asia/Manila,14°40'N,121°03'E,21.0
Maputo,Mozambique,Africa/Maputo,25°58'S,32°32'E,44.0
Maseru,Lesotho,Africa/Maseru,29°18'S,27°30'E,1628.0
Masqat,Oman,Asia/Muscat,23°37'N,58°36'E,8.0
Mbabane,Swaziland,Africa/Mbabane,26°18'S,31°06'E,1243.0
Mecca,Saudi Arabia,Asia/Riyadh,21°26'N,39°49'E,240.0
Medina,Saudi Arabia,Asia/Riyadh,24°28'N,39°36'E,631.0
Mexico,Mexico,America/Mexico_City,19°20'N,99°10'W,2254.0
Minsk,Belarus,Europe/Minsk,53°52'N,27°30'E,231.0
Mogadishu,Somalia,Africa/Mogadishu,02°02'N,45°25'E,9.0
Monaco,Priciplality Of Monaco,Europe/Monaco,43°43'N,7°25'E,206.0
Monrovia,Liberia,Africa/Monrovia,06°18'N,10°47'W,9.0
Montevideo,Uruguay,America/Montevideo,34°50'S,56°11'W,32.0
Moroni,Comoros,Indian/Comoro,11°40'S,43°16'E,29.0
Moscow,Russian Federation,Europe/Moscow,55°45'N,37°35'E,247.0
Moskva,Russian Federation,Europe/Moscow,55°45'N,37°35'E,247.0
Mumbai,India,Asia/Kolkata,18°58'N,72°49'E,14.0
Muscat,Oman,Asia/Muscat,23°37'N,58°32'E,8.0
N'Djamena,Chad,Africa/Ndjamena,12°10'N,14°59'E,295.0
Nairobi,Kenya,Africa/Nairobi,01°17'S,36°48'E,1624.0
Nassau,Bahamas,America/Nassau,25°05'N,77°20'W,7.0
Naypyidaw,Myanmar,Asia/Rangoon,19°45'N,96°6'E,104.0
New Delhi,India,Asia/Kolkata,28°37'N,77°13'E,233.0
Ngerulmud,Palau,Pacific/Palau,7°30'N,134°37'E,3.0
Niamey,Niger,Africa/Niamey,13°27'N,02°06'E,223.0
Nicosia,Cyprus,Asia/Nicosia,35°10'N,33°25'E,162.0
Nouakchott,Mauritania,Africa/Nouakchott,20°10'S,57°30'E,3.0
Noumea,New Caledonia,Pacific/Noumea,22°17'S,166°30'E,69.0
Nuku'alofa,Tonga,Pacific/Tongatapu,21°10'S,174°00'W,6.0
Nuuk,Greenland,America/Godthab,64°10'N,51°35'W,70.0
Oranjestad,Aruba,America/Aruba,12°32'N,70°02'W,33.0
Oslo,Norway,Europe/Oslo,59°55'N,10°45'E,170.0
Ottawa,Canada,US/Eastern,45°27'N,75°42'W,79.0
Ouagadougou,Burkina Faso,Africa/Ouagadougou,12°15'N,01°30'W,316.0
P'yongyang,Democratic People's Republic of Korea,Asia/Pyongyang,39°09'N,125°30'E,21.0
Pago Pago,American Samoa,Pacific/Pago_Pago,14°16'S,170°43'W,0.0
Palikir,Micronesia,Pacific/Ponape,06°55'N,158°09'E,71.0
Panama,Panama,America/Panama,09°00'N,79°25'W,2.0
Papeete,French Polynesia,Pacific/Tahiti,17°32'S,149°34'W,7.0
Paramaribo,Suriname,America/Paramaribo,05°50'N,55°10'W,7.0
Paris,France,Europe/Paris,48°50'N,02°20'E,109.0
Perth,Australia,Australia/Perth,31°56'S,115°50'E,20.0
Phnom Penh,Cambodia,Asia/Phnom_Penh,11°33'N,104°55'E,10.0
Podgorica,Montenegro,Europe/Podgorica,42°28'N,19°16'E,53.0
Port Louis,Mauritius,Indian/Mauritius,20°9'S,57°30'E,5.0
Port Moresby,Papua New Guinea,Pacific/Port_Moresby,09°24'S,147°08'E,44.0
Port-Vila,Vanuatu,Pacific/Efate,17°45'S,168°18'E,1.0
Port-au-Prince,Haiti,America/Port-au-Prince,18°40'N,72°20'W,34.0
Port of Spain,Trinidad and Tobago,America/Port_of_Spain,10°40'N,61°31'W,66.0
Porto-Novo,Benin,Africa/Porto-Novo,06°23'N,02°42'E,38.0
Prague,Czech Republic,Europe/Prague,50°05'N,14°22'E,365.0
Praia,Cape Verde,Atlantic/Cape_Verde,15°02'N,23°34'W,35.0
Pretoria,South Africa,Africa/Johannesburg,25°44'S,28°12'E,1322.0
Pristina,Albania,Europe/Tirane,42°40'N,21°10'E,576.0
Quito,Ecuador,America/Guayaquil,00°15'S,78°35'W,2812.0
Rabat,Morocco,Africa/Casablanca,34°1'N,6°50'W,75.0
Reykjavik,Iceland,Atlantic/Reykjavik,64°10'N,21°57'W,61.0
Riga,Latvia,Europe/Riga,56°53'N,24°08'E,7.0
Riyadh,Saudi Arabia,Asia/Riyadh,24°41'N,46°42'E,612.0
Road Town,British Virgin Islands,America/Virgin,18°27'N,64°37'W,1.0
Rome,Italy,Europe/Rome,41°54'N,12°29'E,95.0
Roseau,Dominica,America/Dominica,15°20'N,61°24'W,72.0
Saint Helier,Jersey,Etc/GMT,49°11'N,2°6'W,54.0
Saint Pierre,Saint Pierre and Miquelon,America/Miquelon,46°46'N,56°12'W,5.0
Saipan,Northern Mariana Islands,Pacific/Saipan,15°12'N,145°45'E,200.0
Sana,Yemen,Asia/Aden,15°20'N,44°12'W,2199.0
Sana'a,Yemen,Asia/Aden,15°20'N,44°12'W,2199.0
San Jose,Costa Rica,America/Costa_Rica,09°55'N,84°02'W,931.0
San Juan,Puerto Rico,America/Puerto_Rico,18°28'N,66°07'W,21.0
San Marino,San Marino,Europe/San_Marino,43°55'N,12°30'E,749.0
San Salvador,El Salvador,America/El_Salvador,13°40'N,89°10'W,621.0
Santiago,Chile,America/Santiago,33°24'S,70°40'W,476.0
Santo Domingo,Dominica Republic,America/Santo_Domingo,18°30'N,69°59'W,14.0
Sao Tome,Sao Tome and Principe,Africa/Sao_Tome,00°10'N,06°39'E,13.0
Sarajevo,Bosnia and Herzegovina,Europe/Sarajevo,43°52'N,18°26'E,511.0
Seoul,Republic of Korea,Asia/Seoul,37°31'N,126°58'E,49.0
Singapore,Republic of Singapore,Asia/Singapore,1°18'N,103°48'E,16.0
Skopje,The Former Yugoslav Republic of Macedonia,Europe/Skopje,42°01'N,21°26'E,238.0
Sofia,Bulgaria,Europe/Sofia,42°45'N,23°20'E,531.0
Sri Jayawardenapura Kotte,Sri Lanka,Asia/Colombo,6°54'N,79°53'E,7.0
St. George's,Grenada,America/Grenada,32°22'N,64°40'W,7.0
St. John's,Antigua and Barbuda,America/Antigua,17°7'N,61°51'W,1.0
St. Peter Port,Guernsey,Europe/Guernsey,49°26'N,02°33'W,1.0
Stanley,Falkland Islands,Atlantic/Stanley,51°40'S,59°51'W,23.0
Stockholm,Sweden,Europe/Stockholm,59°20'N,18°05'E,52.0
Sucre,Bolivia,America/La_Paz,16°20'S,68°10'W,2903.0
Suva,Fiji,Pacific/Fiji,18°06'S,178°30'E,0.0
Sydney,Australia,Australia/Sydney,33°53'S,151°13'E,3.0
Taipei,Republic of China (Taiwan),Asia/Taipei,25°02'N,121°38'E,9.0
T'bilisi,Georgia,Asia/Tbilisi,41°43'N,44°50'E,467.0
Tbilisi,Georgia,Asia/Tbilisi,41°43'N,44°50'E,467.0
Tallinn,Estonia,Europe/Tallinn,59°22'N,24°48'E,39.0
Tarawa,Kiribati,Pacific/Tarawa,01°30'N,173°00'E,2.0
Tashkent,Uzbekistan,Asia/Tashkent,41°20'N,69°10'E,489.0
Tegucigalpa,Honduras,America/Tegucigalpa,14°05'N,87°14'W,994.0
Tehran,Iran,Asia/Tehran,35°44'N,51°30'E,1191.0
Thimphu,Bhutan,Asia/Thimphu,27°31'N,89°45'E,2300.0
Tirana,Albania,Europe/Tirane,41°18'N,19°49'E,90.0
Tirane,Albania,Europe/Tirane,41°18'N,19°49'E,90.0
Torshavn,Faroe Islands,Atlantic/Faroe,62°05'N,06°56'W,39.0
Tokyo,Japan,Asia/Tokyo,35°41'N,139°41'E,8.0
Tripoli,Libyan Arab Jamahiriya,Africa/Tripoli,32°49'N,13°07'E,81.0
Tunis,Tunisia,Africa/Tunis,36°50'N,10°11'E,4.0
Ulan Bator,Mongolia,Asia/Ulaanbaatar,47°55'N,106°55'E,1330.0
Ulaanbaatar,Mongolia,Asia/Ulaanbaatar,47°55'N,106°55'E,1330.0
Vaduz,Liechtenstein,Europe/Vaduz,47°08'N,09°31'E,463.0
Valletta,Malta,Europe/Malta,35°54'N,14°31'E,48.0
Vienna,Austria,Europe/Vienna,48°12'N,16°22'E,171.0
Vientiane,Lao People's Democratic Republic,Asia/Vientiane,17°58'N,102°36'E,171.0
Vilnius,Lithuania,Europe/Vilnius,54°38'N,25°19'E,156.0
W. Indies,Antigua and Barbuda,America/Antigua,17°20'N,61°48'W,0.0
Warsaw,Poland,Europe/Warsaw,52°13'N,21°00'E,107.0
Washington DC,USA,US/Eastern,39°91'N,77°02'W,23.0
Wellington,New Zealand,Pacific/Auckland,41°19'S,174°46'E,7.0
Willemstad,Netherlands Antilles,America/Curacao,12°05'N,69°00'W,1.0
Windhoek,Namibia,Africa/Windhoek,22°35'S,17°04'E,1725.0
Yamoussoukro,Cote d'Ivoire,Africa/Abidjan,06°49'N,05°17'W,213.0
Yangon,Myanmar,Asia/Rangoon,16°45'N,96°20'E,33.0
Yaounde,Cameroon,Africa/Douala,03°50'N,11°35'E,760.0
Yaren,Nauru,Pacific/Nauru,0°32'S,166°55'E,0.0
Yerevan,Armenia,Asia/Yerevan,40°10'N,44°31'E,890.0
Zagreb,Croatia,Europe/Zagreb,45°50'N,15°58'E,123.0

# UK Cities
Aberdeen,Scotland,Europe/London,57°08'N,02°06'W,65.0
Birmingham,England,Europe/London,52°30'N,01°50'W,99.0
Bolton,England,Europe/London,53°35'N,02°15'W,105.0
Bradford,England,Europe/London,53°47'N,01°45'W,127.0
Bristol,England,Europe/London,51°28'N,02°35'W,11.0
Cardiff,Wales,Europe/London,51°29'N,03°13'W,9.0
Crawley,England,Europe/London,51°8'N,00°10'W,77.0
Edinburgh,Scotland,Europe/London,55°57'N,03°13'W,61.0
Glasgow,Scotland,Europe/London,55°50'N,04°15'W,8.0
Greenwich,England,Europe/London,51°28'N,00°00'W,24.0
Leeds,England,Europe/London,53°48'N,01°35'W,47.0
Leicester,England,Europe/London,52°38'N,01°08'W,138.0
Liverpool,England,Europe/London,53°25'N,03°00'W,25.0
Manchester,England,Europe/London,53°30'N,02°15'W,78.0
Newcastle Upon Tyne,England,Europe/London,54°59'N,01°36'W,47.0
Newcastle,England,Europe/London,54°59'N,01°36'W,47.0
Norwich,England,Europe/London,52°38'N,01°18'E,18.0
Oxford,England,Europe/London,51°45'N,01°15'W,72.0
Plymouth,England,Europe/London,50°25'N,04°15'W,50.0
Portsmouth,England,Europe/London,50°48'N,01°05'W,9.0
Reading,England,Europe/London,51°27'N,0°58'W,84.0
Sheffield,England,Europe/London,53°23'N,01°28'W,105.0
Southampton,England,Europe/London,50°55'N,01°25'W,9.0
Swansea,England,Europe/London,51°37'N,03°57'W,91.0
Swindon,England,Europe/London,51°34'N,01°47'W,112.0
Wolverhampton,England,Europe/London,52°35'N,2°08'W,89.0
Barrow-In-Furness,England,Europe/London,54°06'N,3°13'W,20.0

# US State Capitals
Montgomery,USA,US/Central,32°21'N,86°16'W,42.0
Juneau,USA,US/Alaska,58°23'N,134°11'W,29.0
Phoenix,USA,America/Phoenix,33°26'N,112°04'W,331.0
Little Rock,USA,US/Central,34°44'N,92°19'W,95.0
Sacramento,USA,US/Pacific,38°33'N,121°28'W,15.0
Denver,USA,US/Mountain,39°44'N,104°59'W,1600.0
Hartford,USA,US/Eastern,41°45'N,72°41'W,9.0
Dover,USA,US/Eastern,39°09'N,75°31'W,8.0
Tallahassee,USA,US/Eastern,30°27'N,84°16'W,59.0
Atlanta,USA,US/Eastern,33°45'N,84°23'W,267.0
Honolulu,USA,US/Hawaii,21°18'N,157°49'W,229.0
Boise,USA,US/Mountain,43°36'N,116°12'W,808.0
Springfield,USA,US/Central,39°47'N,89°39'W,190.0
Indianapolis,USA,US/Eastern,39°46'N,86°9'W,238.0
Des Moines,USA,US/Central,41°35'N,93°37'W,276.0
Topeka,USA,US/Central,39°03'N,95°41'W,289.0
Frankfort,USA,US/Eastern,38°11'N,84°51'W,243.0
Baton Rouge,USA,US/Central,30°27'N,91°8'W,15.0
Augusta,USA,US/Eastern,44°18'N,69°46'W,41.0
Annapolis,USA,US/Eastern,38°58'N,76°30'W,0.0
Boston,USA,US/Eastern,42°21'N,71°03'W,6.0
Lansing,USA,US/Eastern,42°44'N,84°32'W,271.0
Saint Paul,USA,US/Central,44°56'N,93°05'W,256.0
Jackson,USA,US/Central,32°17'N,90°11'W,90.0
Jefferson City,USA,US/Central,38°34'N,92°10'W,167.0
Helena,USA,US/Mountain,46°35'N,112°1'W,1150.0
Lincoln,USA,US/Central,40°48'N,96°40'W,384.0
Carson City,USA,US/Pacific,39°9'N,119°45'W,1432.0
Concord,USA,US/Eastern,43°12'N,71°32'W,117.0
Trenton,USA,US/Eastern,40°13'N,74°45'W,28.0
Santa Fe,USA,US/Mountain,35°40'N,105°57'W,2151.0
Albany,USA,US/Eastern,42°39'N,73°46'W,17.0
Raleigh,USA,US/Eastern,35°49'N,78°38'W,90.0
Bismarck,USA,US/Central,46°48'N,100°46'W,541.0
Columbus,USA,US/Eastern,39°59'N,82°59'W,271.0
Oklahoma City,USA,US/Central,35°28'N,97°32'W,384.0
Salem,USA,US/Pacific,44°55'N,123°1'W,70.0
Harrisburg,USA,US/Eastern,40°16'N,76°52'W,112.0
Providence,USA,US/Eastern,41°49'N,71°25'W,2.0
Columbia,USA,US/Eastern,34°00'N,81°02'W,96.0
Pierre,USA,US/Central,44°22'N,100°20'W,543.0
Nashville,USA,US/Central,36°10'N,86°47'W,149.0
Austin,USA,US/Central,30°16'N,97°45'W,167.0
Salt Lake City,USA,US/Mountain,40°45'N,111°53'W,1294.0
Montpelier,USA,US/Eastern,44°15'N,72°34'W,325.0
Richmond,USA,US/Eastern,37°32'N,77°25'W,68.0
Olympia,USA,US/Pacific,47°2'N,122°53'W,35.0
Charleston,USA,US/Eastern,38°20'N,81°38'W,11.0
Madison,USA,US/Central,43°4'N,89°24'W,281.0
Cheyenne,USA,US/Mountain,41°8'N,104°48'W,1860.0

# Major US Cities
Birmingham,USA,US/Central,33°39'N,86°48'W,197.0
Anchorage,USA,US/Alaska,61°13'N,149°53'W,30.0
Los Angeles,USA,US/Pacific,34°03'N,118°15'W,50.0
San Francisco,USA,US/Pacific,37°46'N,122°25'W,47.0
Bridgeport,USA,US/Eastern,41°11'N,73°11'W,13.0
Wilmington,USA,US/Eastern,39°44'N,75°32'W,15.0
Jacksonville,USA,US/Eastern,30°19'N,81°39'W,13.0
Miami,USA,US/Eastern,26°8'N,80°12'W,10.0
Chicago,USA,US/Central,41°50'N,87°41'W,189.0
Wichita,USA,US/Central,37°41'N,97°20'W,399.0
Louisville,USA,US/Eastern,38°15'N,85°45'W,142.0
New Orleans,USA,US/Central,29°57'N,90°4'W,10.0
Portland,USA,US/Eastern,43°39'N,70°16'W,6.0
Baltimore,USA,US/Eastern,39°17'N,76°37'W,31.0
Detroit,USA,US/Eastern,42°19'N,83°2'W,189.0
Minneapolis,USA,US/Central,44°58'N,93°15'W,260.0
Kansas City,USA,US/Central,39°06'N,94°35'W,256.0
Billings,USA,US/Mountain,45°47'N,108°32'W,946.0
Omaha,USA,US/Central,41°15'N,96°0'W,299.0
Las Vegas,USA,US/Pacific,36°10'N,115°08'W,720.0
Manchester,USA,US/Eastern,42°59'N,71°27'W,56.0
Newark,USA,US/Eastern,40°44'N,74°11'W,4.0
Albuquerque,USA,US/Mountain,35°06'N,106°36'W,1523.0
New York,USA,US/Eastern,40°43'N,74°0'W,17.0
Charlotte,USA,US/Eastern,35°13'N,80°50'W,217.0
Fargo,USA,US/Central,46°52'N,96°47'W,271.0
Cleveland,USA,US/Eastern,41°28'N,81°40'W,210.0
Philadelphia,USA,US/Eastern,39°57'N,75°10'W,62.0
Sioux Falls,USA,US/Central,43°32'N,96°43'W,443.0
Memphis,USA,US/Central,35°07'N,89°58'W,84.0
Houston,USA,US/Central,29°45'N,95°22'W,8.0
Dallas,USA,US/Central,32°47'N,96°48'W,137.0
Burlington,USA,US/Eastern,44°28'N,73°9'W,35.0
Virginia Beach,USA,US/Eastern,36°50'N,76°05'W,9.0
Seattle,USA,US/Pacific,47°36'N,122°19'W,63.0
Milwaukee,USA,US/Central,43°03'N,87°57'W,188.0
San Diego,USA,US/Pacific,32°42'N,117°09'W,16.0
Orlando,USA,US/Eastern,28°32'N,81°22'W,35.0
Buffalo,USA,US/Eastern,42°54'N,78°50'W,188.0
Toledo,USA,US/Eastern,41°39'N,83°34'W,180.0

# Canadian cities
Vancouver,Canada,America/Vancouver,49°15'N,123°6'W,55.0
Calgary,Canada,America/Edmonton,51°2'N,114°3'W,1040.0
Edmonton,Canada,America/Edmonton,53°32'N,113°29'W,664.0
Saskatoon,Canada,America/Regina,52°8'N,106°40'W,480.0
Regina,Canada,America/Regina,50°27'N,104°36'W,577.0
Winnipeg,Canada,America/Winnipeg,49°53'N,97°8'W,229.0
Toronto,Canada,America/Toronto,43°39'N,79°22'W,77.0
Montreal,Canada,America/Montreal,45°30'N,73°33'W,23.0
Quebec,Canada,America/Toronto,46°48'N,71°14'W,87.0
Fredericton,Canada,America/Halifax,45°57'N,66°38'W,8.0
Halifax,Canada,America/Halifax,44°38'N,63°34'W,36.0
Charlottetown,Canada,America/Halifax,46°14'N,63°7'W,2.0
St. John's,Canada,America/Halifax,47°33'N,52°42'W,116.0
Whitehorse,Canada,America/Whitehorse,60°43'N,135°3'W,696.0
Yellowknife,Canada,America/Yellowknife,62°27'N,114°22'W,191.0
Iqaluit,Canada,America/Iqaluit,63°44'N,68°31'W,3.0
"""
# endregion


_LOCATION_DB: Dict = {}


class LocationGroup(object):
    """Groups a set of timezones by the timezone group"""

    def __init__(self, name):
        self.name = name
        self._locations = {}

    def __getitem__(self, key):
        """Returns a Location object for the specified `key`.

            group = astral.europe
            location = group['London']

        You can supply an optional region name by adding a comma
        followed by the region name. Where multiple locations have the
        same name you may need to supply the region name otherwise
        the first result will be returned which may not be the one
        you're looking for.

            location = group['Abu Dhabi,United Arab Emirates']

        Handles location names with spaces and mixed case.
        """

        key = self._sanitize_key(key)

        try:
            lookup_name, lookup_region = key.split(",", 1)
        except ValueError:
            lookup_name = key
            lookup_region = ""

        lookup_name = lookup_name.strip("\"'")
        lookup_region = lookup_region.strip("\"'")

        for (location_name, location_list) in self._locations.items():
            if location_name == lookup_name:
                if lookup_region == "":
                    return location_list[0]

                for location in location_list:
                    if self._sanitize_key(location.region) == lookup_region:
                        return location

        raise KeyError(f"Unrecognised location name - {key}")

    def __setitem__(self, key, value):
        key = self._sanitize_key(key)
        if key not in self._locations:
            self._locations[key] = [value]
        else:
            self._locations[key].append(value)

    def __contains__(self, key):
        key = self._sanitize_key(key)
        for name in self._locations.keys():
            if name == key:
                return True

        return False

    def __len__(self):
        return len(self._locations)

    def __iter__(self):
        for location_list in self._locations.values():
            for location in location_list:
                yield location

    def keys(self):
        return self._locations.keys()

    def values(self):
        return self._locations.values()

    def items(self):
        return self._locations.items()

    @property
    def locations(self):
        k = []
        for location_list in self._locations.values():
            for location in location_list:
                k.append(location.name)

        return k

    def _sanitize_key(self, key):
        return str(key).lower().replace(" ", "_")


def _init_location_db() -> None:
    if not _LOCATION_DB:
        _add_locations_from_str(_LOCATION_INFO)


def _location_count():
    return reduce(lambda x, y: x + len(y), _LOCATION_DB.values(), 0)


def _add_location_to_db(location_info: LocationInfo) -> None:
    key = location_info.timezone_group.lower()
    group = _LOCATION_DB.get(key, None)
    if not group:
        group = LocationGroup(location_info.timezone_group)
        _LOCATION_DB[key] = group

    group[location_info.name.lower()] = location_info


def _add_locations_from_str(location_string: str) -> None:
    """Add locations from a string."""

    for line in location_string.split("\n"):
        line = line.strip()
        if line != "" and line[0] != "#":
            if line[-1] == "\n":
                line = line[:-1]

            info = line.split(",")
            location = LocationInfo(
                name=info[0],
                region=info[1],
                timezone=info[2],
                latitude=latlng_to_float(info[3]),
                longitude=latlng_to_float(info[4]),
                elevation=float(info[5]),
            )
            _add_location_to_db(location)


def _add_locations_from_list(location_list: List[Tuple]) -> None:
    """Add locations from a list of either strings or lists of strings or tuples of strings."""

    for info in location_list:
        if isinstance(info, str):
            _add_locations_from_str(info)
        elif isinstance(info, (list, tuple)):
            location = LocationInfo(
                name=info[0],
                region=info[1],
                timezone=info[2],
                latitude=latlng_to_float(info[3]),
                longitude=latlng_to_float(info[4]),
                elevation=float(info[5]),
            )
            _add_location_to_db(location)


def add_locations(locations: Union[List, str]) -> None:
    _init_location_db()

    if isinstance(locations, str):
        _add_locations_from_str(locations)
    elif isinstance(locations, (list, tuple)):
        _add_locations_from_list(locations)


def group(key: str) -> LocationGroup:
    """Access to each timezone group. For example London is in timezone
    group Europe.

    Attribute lookup is case insensitive"""

    _init_location_db()

    key = str(key).lower()
    for name, value in _LOCATION_DB.items():
        if name == key:
            return value

    raise AttributeError(f"Unrecognised Group - {key}")


def lookup(key: str) -> LocationInfo:
    _init_location_db()

    key = str(key).lower()
    for group in _LOCATION_DB.values():
        try:
            return group[key]
        except KeyError:
            pass

    raise KeyError(f"Unrecognised location name - {key}")


class Geocoder(object):
    """Looks up geographic information from the locations stored within the
    package
    """

    def add_locations(self, locations: Optional[Union[str, list]] = None) -> None:
        """Add extra locations to Geocoder.

        Extra locations can be

        * A single string containing one or more locations separated by a newline.
        * A list of strings
        * A list of lists/tuples that are passed to a :class:`LocationInfo` constructor
        """

        _init_location_db()

        if isinstance(locations, str):
            self._add_from_str(locations)
        elif isinstance(locations, (list, tuple)):
            self._add_from_list(locations)

    def __getattr__(self, key):
        """Access to each timezone group. For example London is in timezone
        group Europe.

        Attribute lookup is case insensitive"""

        return group(key)

    def __getitem__(self, key: str) -> LocationInfo:
        """Lookup a location within all timezone groups.

        Item lookup is case insensitive."""

        return lookup(key)

    def __iter__(self):
        return _LOCATION_DB.__iter__()

    def __contains__(self, key):
        key = str(key).lower()
        for name, group in _LOCATION_DB.items():
            if name == key:
                return True

            if key in group:
                return True

        return False

    @property
    def locations(self):
        k = []
        for group in _LOCATION_DB.values():
            k.extend(group.locations)

        return k

    @property
    def groups(self):
        return _LOCATION_DB
