#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: core/preflight/gps.py
Version: 1.0.0 (Kwetal)
Role: Utility - Location Provider
Objective: Manages geographic coordinates using config.toml as the source of truth.
"""

from astropy.coordinates import EarthLocation
import astropy.units as u
import tomllib
from pathlib import Path

class GPSLocation:
    def __init__(self):
        # Always pull from the central config.toml
        config_path = Path(__file__).parent.parent.parent / "config.toml"
        with open(config_path, "rb") as f:
            cfg = tomllib.load(f)
        
        self.lat = float(cfg['location']['latitude'])
        self.lon = float(cfg['location']['longitude'])
        self.height = float(cfg['location']['elevation'])

    def get_earth_location(self):
        return EarthLocation(lat=self.lat*u.deg, lon=self.lon*u.deg, height=self.height*u.m)

gps_location = GPSLocation()
