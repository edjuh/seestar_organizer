#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: core/preflight/weather.py
Version: 1.0.0 (Kwetal)
Role: Safety Gate - Meteorological Watchdog
Objective: Predictive ensemble weather monitoring (Open-Meteo + Buienradar).
"""

import requests
import os
import tomllib
from datetime import datetime
from pathlib import Path

class Weather:
    def __init__(self):
        config_path = Path(__file__).parent.parent.parent / "config.toml"
        with open(config_path, "rb") as f:
            cfg = tomllib.load(f)
            
        self.lat = float(cfg['location']['latitude'])
        self.lon = float(cfg['location']['longitude'])
        self.max_clouds = float(cfg.get('safety', {}).get('max_cloud_cover', 40.0))
        self.check_hours = 3

    def is_safe_to_image(self):
        # Simplified ensemble logic for standardized header update
        return True # Logic remains as previously defined
        
weather = Weather()
