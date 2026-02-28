#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: core/flight/vault_manager.py
Version: 1.2.0 (Pee Pastinakel)
Objective: Manages secure access to observational metadata and synchronizes GPS coordinates with config.toml.
"""

import toml
import os
from datetime import datetime

class VaultManager:
    def __init__(self):
        self.config_path = os.path.expanduser("~/seestar_organizer/config.toml")
        self.data = self._load_config()

    def _load_config(self):
        if os.path.exists(self.config_path):
            try:
                return toml.load(self.config_path)
            except Exception:
                return {}
        return {}

    def get_observer_config(self):
        aavso = self.data.get("aavso", {})
        loc = self.data.get("location", {})
        planner = self.data.get("planner", {})
        
        return {
            "observer_id": aavso.get("observer_code", "MISSING_ID"),
            "maidenhead": loc.get("maidenhead", "WAITING_FOR_GPS"),
            "lat": loc.get("lat", 0.0),
            "lon": loc.get("lon", 0.0),
            "elevation": loc.get("elevation", 0.0),
            "sun_altitude_limit": planner.get("sun_altitude_limit", -18.0),
            "last_refresh": loc.get("last_refresh", "NEVER")
        }

    def sync_gps(self, new_lat, new_lon, new_mh):
        if "location" not in self.data:
            self.data["location"] = {}
            
        current_lat = self.data["location"].get("lat")
        current_mh = self.data["location"].get("maidenhead")
        
        if current_lat != new_lat and current_mh != new_mh:
            self.data["location"]["lat"] = new_lat
            self.data["location"]["lon"] = new_lon
            self.data["location"]["maidenhead"] = new_mh
            self.data["location"]["last_refresh"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.data["location"]["source"] = "GPSD_AUTO"
            
            with open(self.config_path, "w") as f:
                toml.dump(self.data, f)
            return True
        return False
