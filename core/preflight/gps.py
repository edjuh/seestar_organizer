#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Objective: Manages geographic coordinates using config.toml as the source of truth.
"""
"""
Filename: core/preflight/gps.py
Version: 1.0.0 (Kwetal)
Role: Utility - Location Provider
"""

import tomllib
from pathlib import Path
from astropy.coordinates import EarthLocation
import astropy.units as u

class GPSLocation:
    def __init__(self):
        config_path = Path(__file__).parent.parent.parent / "config.toml"
        with open(config_path, "rb") as f:
            cfg = tomllib.load(f)
        
        # Aligning with short-keys found in your config.toml
        loc = cfg.get('location', {})
        self.lat = float(loc.get('lat', 52.3874))
        self.lon = float(loc.get('lon', 4.6462))
        self.height = float(loc.get('elevation', 0.0))

    def get_earth_location(self):
        return EarthLocation(lat=self.lat*u.deg, lon=self.lon*u.deg, height=self.height*u.m)

gps_location = GPSLocation()
