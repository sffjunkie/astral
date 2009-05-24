
    def solar_elevation(self, dateandtime, latitude, longitude):
        """Calculate the elevation of the sun as a specific date/time and location
        
        Result will be returned in the time zone of `dateandtime`
        """
        
        if latitude > 89.8:
            latitude = 89.8
            
        if latitude < -89.8:
            latitude = -89.8
            
        # Change time zone to positive hours in western hemisphere
        zone = -tz_offset
        daySavings = dlstime * 60
        hh = hours - (daySavings / 60)
        mm = minutes
        ss = seconds

        #    timenow is GMT time for calculation in hours since 0Z
        timenow = hh + mm / 60 + ss / 3600 + zone

        JD = self._julianday(date.day, date.month, date.year)
        t = _jday_to_jcentury(JD + timenow / 24.0)
        R = self._sun_rad_vector(t)
        alpha = self._sun_rt_ascension(t)
        theta = self._sun_declination(t)
        Etime = self._eq_of_time(t)

        eqtime = Etime
        solarDec = theta   # in degrees
        earthRadVec = R

        solarTimeFix = eqtime - 4.0 * longitude + 60# * zone
        trueSolarTime = hh * 60.0 + mm + ss / 60.0 + solarTimeFix
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

#beginning of complex expression commented out
#            If (exoatmElevation > 85#) Then
#                refractionCorrection = 0#
#            Else
#                te = Tan(degToRad(exoatmElevation))
#                If (exoatmElevation > 5#) Then
#                    refractionCorrection = 58.1 / te - 0.07 / (te * te * te) + _
#                        0.000086 / (te * te * te * te * te)
#                ElseIf (exoatmElevation > -0.575) Then
#                    refractionCorrection = 1735# + exoatmElevation * _
#                        (-518.2 + exoatmElevation * (103.4 + _
#                        exoatmElevation * (-12.79 + _
#                        exoatmElevation * 0.711)))
#                Else
#                    refractionCorrection = -20.774 / te
#                End If
#                refractionCorrection = refractionCorrection / 3600#
#            End If
#end of complex expression

#beginning of simplified expression
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
#end of simplified expression
            
        solarzen = zenith - refractionCorrection
                     
#            If (solarZen < 108.0) Then
#              solarazimuth = azimuth
        solarelevation = 90.0 - solarzen
#              If (solarZen < 90.0) Then
#                coszen = Cos(degToRad(solarZen))
#              Else
#                coszen = 0#
#              End If
#            Else    #// do not report az & el after astro twilight
#              solarazimuth = -999999
#              solarelevation = -999999
#              coszen = -999999
#            End If

        return solarelevation

