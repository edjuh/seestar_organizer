"""
Filename: core/gps.py
Objective: Manages geographic coordinates for astronomical calculations.
Usage: from core.gps import gps_location; loc = gps_location.get_earth_location()
Note: Defaults to Haarlem, NL coordinates if no hardware GPS is detected.
"""
from astropy.coordinates import EarthLocation
import astropy.units as u
from core.env_loader import cfg

class GPSLocation:
    def __init__(self):
        self.lat = float(cfg("LATITUDE", 52.3873))
        self.lon = float(cfg("LONGITUDE", 4.6462))
        self.height = float(cfg("HEIGHT", 0))

    def get_earth_location(self):
        return EarthLocation(lat=self.lat*u.deg, lon=self.lon*u.deg, height=self.height*u.m)

gps_location = GPSLocation()
