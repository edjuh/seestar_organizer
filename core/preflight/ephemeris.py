"""
Filename: core/ephemeris.py
Objective: Solar, lunar, and stellar position calculator for Haarlem coordinates.
"""
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, get_sun
from astropy.time import Time
import astropy.units as u
from core.env_loader import cfg

class EphemerisEngine:
    def __init__(self):
        self.lat = float(cfg("LATITUDE", 52.38))
        self.lon = float(cfg("LONGITUDE", 4.64))
        self.location = EarthLocation(lat=self.lat*u.deg, lon=self.lon*u.deg, height=0*u.m)

    def is_dark_enough(self):
        now = Time.now()
        altaz_frame = AltAz(obstime=now, location=self.location)
        self.sun_alt = get_sun(now).transform_to(altaz_frame).alt.degree
        return self.sun_alt < -12.0

    def get_alt_az(self, ra, dec, time_override=None):
        """Converts RA/Dec to Alt/Az for 'now' or a specific Time object."""
        check_time = time_override if time_override else Time.now()
        
        if isinstance(ra, str) and ":" in ra:
            target = SkyCoord(ra, dec, unit=(u.hourangle, u.deg), frame='icrs')
        else:
            target = SkyCoord(ra, dec, unit=(u.deg, u.deg), frame='icrs')
        
        altaz_frame = AltAz(obstime=check_time, location=self.location)
        target_altaz = target.transform_to(altaz_frame)
        return {"alt": target_altaz.alt.degree, "az": target_altaz.az.degree}

observer = EphemerisEngine()
