import dataclasses
import datetime
from typing import Tuple, Union, Optional

import pytz

import astral.moon
import astral.calc
import astral.local
import astral.utc
from astral import AstralError, LocationInfo, Observer, SunDirection, latlng_to_float


class Location:
    """Provides access to information for single location."""

    def __init__(self, info: LocationInfo = None):
        """Initializes the object with a LocationInfo object.

            The tuple should contain items in the following order

            ================ =============
            Field            Default
            ================ =============
            name             Greenwich
            region           England
            latitude         51.4733
            longitude        -0.00088
            time zone name   Europe/London
            elevation        24
            ================ =============

            See :attr:`timezone` property for a method of obtaining time zone
            names
        """

        self._location_info: LocationInfo
        self._solar_depression: float = 6.0

        if not info:
            self._location_info = LocationInfo(
                "Greenwich", "England", "Europe/London", 51.4733, -0.00088, 24
            )
        else:
            self._location_info = info

    def __eq__(self, other: object) -> bool:
        if type(other) is LocationInfo:
            return self._location_info == other
        return NotImplemented

    def __repr__(self) -> str:
        if self.region:
            _repr = "%s/%s" % (self.name, self.region)
        else:
            _repr = self.name
        return f"{_repr}, tz={self.timezone}, lat={self.latitude:0.02f}, lon={self.longitude:0.02f}"

    @property
    def info(self) -> LocationInfo:
        return LocationInfo(
            self.name,
            self.region,
            self.timezone,
            self.latitude,
            self.longitude,
            self.elevation,
        )

    @property
    def name(self) -> str:
        return self._location_info.name

    @name.setter
    def name(self, name: str) -> None:
        self._location_info = dataclasses.replace(self._location_info, name=name)

    @property
    def region(self) -> str:
        return self._location_info.region

    @region.setter
    def region(self, region: str) -> None:
        self._location_info = dataclasses.replace(self._location_info, region=region)

    @property
    def latitude(self) -> float:
        """The location's latitude

        ``latitude`` can be set either as a string or as a number

        For strings they must be of the form

            degrees°minutes'[N|S] e.g. 51°31'N

        For numbers, positive numbers signify latitudes to the North.
        """

        return self._location_info.latitude

    @latitude.setter
    def latitude(self, latitude: Union[float, str]) -> None:
        if isinstance(latitude, str):
            _latitude = latlng_to_float(latitude)
        else:
            _latitude = float(latitude)

        self._location_info = dataclasses.replace(
            self._location_info, latitude=_latitude
        )

    @property
    def longitude(self) -> float:
        """The location's longitude.

        ``longitude`` can be set either as a string or as a number

        For strings they must be of the form

            degrees°minutes'[E|W] e.g. 51°31'W

        For numbers, positive numbers signify longitudes to the East.
        """

        return self._location_info.longitude

    @longitude.setter
    def longitude(self, longitude: Union[float, str]) -> None:
        if isinstance(longitude, str):
            _longitude = latlng_to_float(longitude)
        else:
            _longitude = float(longitude)

        self._location_info = dataclasses.replace(
            self._location_info, longitude=_longitude
        )

    @property
    def elevation(self) -> float:
        """The elevation in metres above sea level."""

        return self._location_info.elevation

    @elevation.setter
    def elevation(self, elevation: float) -> None:
        elevation = int(elevation)
        self._location_info = dataclasses.replace(
            self._location_info, elevation=elevation
        )

    @property
    def timezone(self) -> str:
        """The name of the time zone for the location.

        A list of time zone names can be obtained from pytz. For example.

        >>> from pytz import all_timezones
        >>> for timezone in all_timezones:
        ...     print(timezone)
        """

        return self._location_info.timezone

    @timezone.setter
    def timezone(self, name: str) -> None:
        if name not in pytz.all_timezones:
            raise ValueError("Timezone '%s' not recognized" % name)

        self._location_info = dataclasses.replace(self._location_info, timezone=name)

    @property
    def tz(self) -> pytz.tzinfo:  # type: ignore
        """Time zone information."""

        try:
            tz = pytz.timezone(self._location_info.timezone)
            return tz
        except pytz.UnknownTimeZoneError:
            raise AstralError("Unknown timezone '%s'" % self.timezone)

    tzinfo = tz

    @property
    def solar_depression(self) -> float:
        """The number of degrees the sun must be below the horizon for the
        dawn/dusk calculation.

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

        return self._solar_depression

    @solar_depression.setter
    def solar_depression(self, depression: Union[float, str]) -> None:
        if isinstance(depression, str):
            try:
                self._solar_depression = {
                    "civil": 6.0,
                    "nautical": 12.0,
                    "astronomical": 18.0,
                }[depression]
            except KeyError:
                raise KeyError(
                    (
                        "solar_depression must be either a number "
                        "or one of 'civil', 'nautical' or "
                        "'astronomical'"
                    )
                )
        else:
            self._solar_depression = float(depression)

    def today(self, local: bool = True) -> datetime.date:
        if local:
            return astral.local.today(self.tzinfo)
        else:
            return astral.utc.today()

    def sun(
        self, date: datetime.date = None, local: bool = True, use_elevation: bool = True
    ) -> dict:
        """Returns dawn, sunrise, noon, sunset and dusk as a dictionary.

        :param date: The date for which to calculate the times.
                     If no date is specified then the current date will be used.

        :param local: True  = Time to be returned in location's time zone;
                      False = Time to be returned in UTC.
                      If not specified then the time will be returned in local time

        :param use_elevation: True  = Return times that allow for the location's elevation;
                              False = Return times that don't use elevation.
                              If not specified then times will take elevation into account.

        :returns: Dictionary with keys ``dawn``, ``sunrise``, ``noon``,
            ``sunset`` and ``dusk`` whose values are the results of the
            corresponding methods.
         """

        if local and self.timezone is None:
            raise ValueError("Local time requested but Location has no timezone set.")

        if date is None:
            date = self.today(local)

        elevation = self.elevation if use_elevation else 0
        observer = Observer(self.latitude, self.longitude, elevation)

        if local:
            return astral.local.sun(observer, date, self.solar_depression, self.tzinfo)
        else:
            return astral.utc.sun(observer, date, self.solar_depression)

    def dawn(
        self, date: datetime.date = None, local: bool = True, use_elevation: bool = True
    ) -> datetime.datetime:
        """Calculates the time in the morning when the sun is a certain number
        of degrees below the horizon. By default this is 6 degrees but can be
        changed by setting the :attr:`Astral.solar_depression` property.

        :param date: The date for which to calculate the dawn time.
                     If no date is specified then the current date will be used.

        :param local: True  = Time to be returned in location's time zone;
                      False = Time to be returned in UTC.
                      If not specified then the time will be returned in local time

        :param use_elevation: True  = Return times that allow for the location's elevation;
                              False = Return times that don't use elevation.
                              If not specified then times will take elevation into account.

        :returns: The date and time at which dawn occurs.
        """

        if local and self.timezone is None:
            raise ValueError("Local time requested but Location has no timezone set.")

        if date is None:
            date = self.today(local)

        elevation = self.elevation if use_elevation else 0
        observer = Observer(self.latitude, self.longitude, elevation)

        if local:
            return astral.local.dawn(observer, date, self.solar_depression, self.tzinfo)
        else:
            return astral.utc.dawn(observer, date, self.solar_depression)

    def sunrise(
        self, date: datetime.date = None, local: bool = True, use_elevation: bool = True
    ) -> datetime.datetime:
        """Return sunrise time.

        Calculates the time in the morning when the sun is a 0.833 degrees
        below the horizon. This is to account for refraction.

        :param date: The date for which to calculate the sunrise time.
                     If no date is specified then the current date will be used.

        :param local: True  = Time to be returned in location's time zone;
                      False = Time to be returned in UTC.
                      If not specified then the time will be returned in local time
        :type local:  bool

        :param use_elevation: True  = Return times that allow for the location's elevation;
                              False = Return times that don't use elevation.
                              If not specified then times will take elevation into account.
        :type use_elevation:  bool

        :returns: The date and time at which sunrise occurs.
        """

        if local and self.timezone is None:
            raise ValueError("Local time requested but Location has no timezone set.")

        if date is None:
            date = self.today(local)

        elevation = self.elevation if use_elevation else 0
        observer = Observer(self.latitude, self.longitude, elevation)

        if local:
            return astral.local.sunrise(observer, date, self.tzinfo)
        else:
            return astral.utc.sunrise(observer, date)

    def solar_noon(
        self, date: datetime.date = None, local: bool = True
    ) -> datetime.datetime:
        """Calculates the solar noon (the time when the sun is at its highest
        point.)

        :param date: The date for which to calculate the noon time.
                     If no date is specified then the current date will be used.

        :param local: True  = Time to be returned in location's time zone;
                      False = Time to be returned in UTC.
                      If not specified then the time will be returned in local time

        :returns: The date and time at which the solar noon occurs.
        """

        if local and self.timezone is None:
            raise ValueError("Local time requested but Location has no timezone set.")

        if date is None:
            date = self.today(local)

        observer = Observer(self.latitude, self.longitude)
        if local:
            return astral.local.solar_noon(observer, date, self.tzinfo)
        else:
            return astral.utc.solar_noon(observer, date)

    def sunset(
        self, date: datetime.date = None, local: bool = True, use_elevation: bool = True
    ) -> datetime.datetime:
        """Calculates sunset time (the time in the evening when the sun is a
        0.833 degrees below the horizon. This is to account for refraction.)

        :param date: The date for which to calculate the sunset time.
                     If no date is specified then the current date will be used.

        :param local: True  = Time to be returned in location's time zone;
                      False = Time to be returned in UTC.
                      If not specified then the time will be returned in local time
        :type local:  bool

        :param use_elevation: True  = Return times that allow for the location's elevation;
                              False = Return times that don't use elevation.
                              If not specified then times will take elevation into account.
        :type use_elevation:  bool

        :returns: The date and time at which sunset occurs.
        """

        if local and self.timezone is None:
            raise ValueError("Local time requested but Location has no timezone set.")

        if date is None:
            date = self.today(local)

        elevation = self.elevation if use_elevation else 0
        observer = Observer(self.latitude, self.longitude, elevation)

        if local:
            return astral.local.sunset(observer, date, self.tzinfo)
        else:
            return astral.utc.sunset(observer, date)

    def dusk(
        self, date: datetime.date = None, local: bool = True, use_elevation: bool = True
    ) -> datetime.datetime:
        """Calculates the dusk time (the time in the evening when the sun is a
        certain number of degrees below the horizon. By default this is 6
        degrees but can be changed by setting the
        :attr:`solar_depression` property.)

        :param date: The date for which to calculate the dusk time.
                     If no date is specified then the current date will be used.

        :param local: True  = Time to be returned in location's time zone;
                      False = Time to be returned in UTC.
                      If not specified then the time will be returned in local time

        :param use_elevation: True  = Return times that allow for the location's elevation;
                              False = Return times that don't use elevation.
                              If not specified then times will take elevation into account.

        :returns: The date and time at which dusk occurs.
        """

        if local and self.timezone is None:
            raise ValueError("Local time requested but Location has no timezone set.")

        if date is None:
            date = self.today(local)

        elevation = self.elevation if use_elevation else 0
        observer = Observer(self.latitude, self.longitude, elevation)

        if local:
            return astral.local.dusk(observer, date, self.solar_depression, self.tzinfo)
        else:
            return astral.utc.dusk(observer, date, self.solar_depression)

    def solar_midnight(
        self, date: datetime.date = None, local: bool = True
    ) -> datetime.datetime:
        """Calculates the solar midnight (the time when the sun is at its lowest
        point.)

        :param date: The date for which to calculate the midnight time.
                     If no date is specified then the current date will be used.

        :param local: True  = Time to be returned in location's time zone;
                      False = Time to be returned in UTC.
                      If not specified then the time will be returned in local time

        :returns: The date and time at which the solar midnight occurs.
        """

        if local and self.timezone is None:
            raise ValueError("Local time requested but Location has no timezone set.")

        if date is None:
            date = self.today(local)

        observer = Observer(self.latitude, self.longitude)

        if local:
            return astral.local.solar_midnight(observer, date, self.tzinfo)
        else:
            return astral.utc.solar_midnight(observer, date)

    def daylight(
        self, date: datetime.date = None, local: bool = True, use_elevation: bool = True
    ) -> Tuple[datetime.datetime, datetime.datetime]:
        """Calculates the daylight time (the time between sunrise and sunset)

        :param date: The date for which to calculate daylight.
                     If no date is specified then the current date will be used.

        :param local: True  = Time to be returned in location's time zone;
                      False = Time to be returned in UTC.
                      If not specified then the time will be returned in local time
        :type local:  bool

        :param use_elevation: True  = Return times that allow for the location's elevation;
                              False = Return times that don't use elevation.
                              If not specified then times will take elevation into account.
        :type use_elevation:  bool

        :returns: A tuple containing the start and end times
        """

        if local and self.timezone is None:
            raise ValueError("Local time requested but Location has no timezone set.")

        if date is None:
            date = self.today(local)

        elevation = self.elevation if use_elevation else 0
        observer = Observer(self.latitude, self.longitude, elevation)

        if local:
            return astral.local.daylight(observer, date, self.tzinfo)
        else:
            return astral.utc.daylight(observer, date)

    def night(
        self, date: datetime.date = None, local: bool = True, use_elevation: bool = True
    ) -> Tuple[datetime.datetime, datetime.datetime]:
        """Calculates the night time (the time between astronomical dusk and
        astronomical dawn of the next day)

        :param date: The date for which to calculate the start of the night time.
                     If no date is specified then the current date will be used.

        :param local: True  = Time to be returned in location's time zone;
                      False = Time to be returned in UTC.
                      If not specified then the time will be returned in local time

        :param use_elevation: True  = Return times that allow for the location's elevation;
                              False = Return times that don't use elevation.
                              If not specified then times will take elevation into account.

        :returns: A tuple containing the start and end times
        """

        if local and self.timezone is None:
            raise ValueError("Local time requested but Location has no timezone set.")

        if date is None:
            date = self.today(local)

        elevation = self.elevation if use_elevation else 0
        observer = Observer(self.latitude, self.longitude, elevation)

        if local:
            return astral.local.night(observer, date, self.tzinfo)
        else:
            return astral.utc.night(observer, date)

    def twilight(
        self,
        direction: SunDirection = SunDirection.RISING,
        date: datetime.date = None,
        local: bool = True,
        use_elevation: bool = True,
    ):
        """Returns the start and end times of Twilight in the UTC timezone when
        the sun is traversing in the specified direction.

        This method defines twilight as being between the time
        when the sun is at -6 degrees and sunrise/sunset.

        :param direction:  Determines whether the time is for the sun rising or setting.
                           Use ``astral.SUN_RISING`` or ``astral.SunDirection.SETTING``.
        :type direction:   int

        :param date: The date for which to calculate the times.

        :param local: True  = Time to be returned in location's time zone;
                      False = Time to be returned in UTC.
                      If not specified then the time will be returned in local time
        :type local:  bool

        :param use_elevation: True  = Return times that allow for the location's elevation;
                              False = Return times that don't use elevation.
                              If not specified then times will take elevation into account.
        :type use_elevation:  bool

        :return: A tuple of the UTC date and time at which twilight starts and ends.
        """

        if local and self.timezone is None:
            raise ValueError("Local time requested but Location has no timezone set.")

        if date is None:
            date = self.today(local)

        elevation = self.elevation if use_elevation else 0
        observer = Observer(self.latitude, self.longitude, elevation)

        if local:
            return astral.local.twilight(observer, date, direction, self.tzinfo)
        else:
            return astral.utc.twilight(observer, date, direction)

    def time_at_altitude(
        self,
        altitude: float,
        date: datetime.date = None,
        direction: SunDirection = SunDirection.RISING,
        local: bool = True,
    ) -> datetime.datetime:
        """Calculate the time when the sun is at the specified altitude.

        Note:
            This method uses positive altitudes for those above the horizon.

            Elevations greater than 90 degrees are converted to a setting sun
            i.e. an altitude of 110 will calculate a setting sun at 70 degrees.

        :param altitude:  Elevation in degrees above the horizon to calculate for.
        :param direction:  Determines whether the time is for the sun rising or setting.
                           Use ``SunDirection.RISING`` or ``SunDirection.SETTING``.
                           Default is rising.

        :param date: The date for which to calculate the altitude time.
                     If no date is specified then the current date will be used.

        :param local: True  = Time to be returned in location's time zone;
                      False = Time to be returned in UTC.
                      If not specified then the time will be returned in local time

        :returns: The date and time at which dusk occurs.
        """

        if local and self.timezone is None:
            raise ValueError("Local time requested but Location has no timezone set.")

        if date is None:
            date = self.today(local)

        if altitude > 90.0:
            altitude = 180.0 - altitude
            direction = SunDirection.SETTING

        observer = Observer(self.latitude, self.longitude, altitude)

        if local:
            return astral.local.time_at_altitude(
                observer, altitude, date, direction, self.tzinfo
            )
        else:
            return astral.utc.time_at_altitude(observer, altitude, date, direction)

    def rahukaalam(
        self, date: datetime.date = None, local: bool = True, use_elevation: bool = True
    ) -> Tuple[datetime.datetime, datetime.datetime]:
        """Calculates the period of rahukaalam.

        :param date: The date for which to calculate the rahukaalam period.
                     A value of ``None`` uses the current date.

        :param local: True  = Time to be returned in location's time zone;
                      False = Time to be returned in UTC.
        :type local:  bool

        :param use_elevation: True  = Return times that allow for the location's elevation;
                              False = Return times that don't use elevation.
                              If not specified then times will take elevation into account.
        :type use_elevation:  bool

        :return: Tuple containing the start and end times for Rahukaalam.
        """

        if local and self.timezone is None:
            raise ValueError("Local time requested but Location has no timezone set.")

        if date is None:
            date = self.today(local)

        elevation = self.elevation if use_elevation else 0
        observer = Observer(self.latitude, self.longitude, elevation)

        if local:
            return astral.local.rahukaalam(observer, date, self.tzinfo)
        else:
            return astral.utc.rahukaalam(observer, date)

    def golden_hour(
        self,
        direction: SunDirection = SunDirection.RISING,
        date: datetime.date = None,
        local: bool = True,
        use_elevation: bool = True,
    ) -> Tuple[datetime.datetime, datetime.datetime]:
        """Returns the start and end times of the Golden Hour when the sun is traversing
        in the specified direction.

        This method uses the definition from PhotoPills i.e. the
        golden hour is when the sun is between 4 degrees below the horizon
        and 6 degrees above.

        :param direction:  Determines whether the time is for the sun rising or setting.
                           Use ``SunDirection.RISING`` or ``SunDirection.SETTING``.
                           Default is rising.

        :param date: The date for which to calculate the times.

        :param local: True  = Times to be returned in location's time zone;
                      False = Times to be returned in UTC.
                      If not specified then the time will be returned in local time

        :param use_elevation: True  = Return times that allow for the location's elevation;
                              False = Return times that don't use elevation.
                              If not specified then times will take elevation into account.

        :return: A tuple of the date and time at which the Golden Hour starts and ends.
        """

        if local and self.timezone is None:
            raise ValueError("Local time requested but Location has no timezone set.")

        if date is None:
            date = self.today(local)

        elevation = self.elevation if use_elevation else 0
        observer = Observer(self.latitude, self.longitude, elevation)

        if local:
            return astral.local.golden_hour(observer, date, direction, self.tzinfo)
        else:
            return astral.utc.golden_hour(observer, date, direction)

    def blue_hour(
        self,
        direction: SunDirection = SunDirection.RISING,
        date: datetime.date = None,
        local: bool = True,
        use_elevation: bool = True,
    ) -> Tuple[datetime.datetime, datetime.datetime]:
        """Returns the start and end times of the Blue Hour when the sun is traversing
        in the specified direction.

        This method uses the definition from PhotoPills i.e. the
        blue hour is when the sun is between 6 and 4 degrees below the horizon.

        :param direction:  Determines whether the time is for the sun rising or setting.
                           Use ``SunDirection.RISING`` or ``SunDirection.SETTING``.
                           Default is rising.

        :param date: The date for which to calculate the times.
                     If no date is specified then the current date will be used.

        :param local: True  = Times to be returned in location's time zone;
                      False = Times to be returned in UTC.
                      If not specified then the time will be returned in local time

        :param use_elevation: True  = Return times that allow for the location's elevation;
                              False = Return times that don't use elevation.
                              If not specified then times will take elevation into account.

        :return: A tuple of the date and time at which the Blue Hour starts and ends.
        """

        if local and self.timezone is None:
            raise ValueError("Local time requested but Location has no timezone set.")

        if date is None:
            date = self.today(local)

        elevation = self.elevation if use_elevation else 0
        observer = Observer(self.latitude, self.longitude, elevation)

        if local:
            return astral.local.blue_hour(observer, date, direction, self.tzinfo)
        else:
            return astral.utc.blue_hour(observer, date, direction)

    def solar_azimuth(self, dateandtime: datetime.datetime = None) -> float:
        """Calculates the solar azimuth angle for a specific date/time.

        :param dateandtime: The date and time for which to calculate the angle.
        :returns: The azimuth angle in degrees clockwise from North.
        """

        if dateandtime is None:
            dateandtime = astral.local.now(self.tzinfo)
        elif not dateandtime.tzinfo:
            dateandtime = self.tzinfo.localize(dateandtime)

        dateandtime = dateandtime.astimezone(pytz.utc)
        return astral.calc.azimuth(dateandtime, self.latitude, self.longitude)

    def solar_elevation(self, dateandtime: datetime.datetime = None) -> float:
        """Calculates the solar elevation angle for a specific time.

        :param dateandtime: The date and time for which to calculate the angle.

        :returns: The elevation angle in degrees above the horizon.
        """

        if dateandtime is None:
            dateandtime = astral.local.now(self.tzinfo)
        elif not dateandtime.tzinfo:
            dateandtime = self.tzinfo.localize(dateandtime)

        dateandtime = dateandtime.astimezone(pytz.utc)
        return astral.calc.altitude(dateandtime, self.latitude, self.longitude)

    def solar_zenith(self, dateandtime: datetime.datetime) -> float:
        """Calculates the solar zenith angle for a specific time.

        :param dateandtime: The date and time for which to calculate the angle.
        :returns: The zenith angle in degrees from vertical.
        """

        return 90.0 - self.solar_elevation(dateandtime)

    def moon_phase(
        self, date: datetime.date = None, local: bool = True, rtype: type = int
    ):
        """Calculates the moon phase for a specific date.

        :param date: The date to calculate the phase for. If ommitted the current date is used.

        :returns:
            A number designating the phase

                | 0  = New moon
                | 7  = First quarter
                | 14 = Full moon
                | 21 = Last quarter
        """

        if date is None:
            date = self.today(local)

        return astral.moon.phase(date, rtype)
