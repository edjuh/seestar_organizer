"""
Filename: core/target_manager.py
Version: 1.1.0
Purpose: AAVSO Target Selection with Dynamic GPS Updates.
"""
import requests
import json
from datetime import datetime
from astropy.coordinates import SkyCoord, AltAz, EarthLocation
from astropy.time import Time
import astropy.units as u

class TargetManager:
    def __init__(self, config: dict):
        # Default coordinates from config
        self.lat = config.get("lat", 52.38)
        self.lon = config.get("lon", 4.64)
        self.elevation = config.get("elevation", 0)
        self.min_alt = config.get("min_alt", 30)
        self.api_key = config.get("target_tool_key", "")
        
        # Hardcoded AAVSO Target List (or load from file)
        self.catalog = [
            {"name": "AX Per", "ra": "01:36:22.7", "dec": "+54:15:02", "comp_stars": ["115", "118", "121"]},
            {"name": "SS Cyg", "ra": "21:42:42.8", "dec": "+43:35:10", "comp_stars": ["123", "126"]},
            {"name": "V Sge",  "ra": "20:20:14.7", "dec": "+21:06:10", "comp_stars": ["108", "112"]},
            {"name": "Z Cam",  "ra": "08:25:13.2", "dec": "+73:06:39", "comp_stars": ["110", "115"]}
        ]

    def update_location(self, lat, lon, alt=None):
        """Dynamic update from GPS thread."""
        try:
            self.lat = float(lat)
            self.lon = float(lon)
            if alt is not None:
                self.elevation = float(alt)
            print(f"[BRAIN] Coordinates synchronized: {self.lat}, {self.lon}")
        except Exception as e:
            print(f"[BRAIN] Location update failed: {e}")

    def get_observer_location(self):
        return EarthLocation(lat=self.lat*u.deg, lon=self.lon*u.deg, height=self.elevation*u.m)

    def process_catalog(self, strategy="priority"):
        """Calculates altitude for all targets and filters by visibility."""
        observer = self.get_observer_location()
        now = Time(datetime.utcnow())
        altaz_frame = AltAz(obstime=now, location=observer)
        
        observable = []
        
        for entry in self.catalog:
            try:
                # Convert RA/Dec strings to SkyCoord
                coord = SkyCoord(entry['ra'], entry['dec'], unit=(u.hourangle, u.deg))
                target_altaz = coord.transform_to(altaz_frame)
                
                alt = target_altaz.alt.degree
                
                if alt > self.min_alt:
                    # Enrich target data with current altitude
                    target_data = entry.copy()
                    target_data['current_alt'] = round(alt, 2)
                    target_data['ra_deg'] = coord.ra.degree
                    target_data['dec_deg'] = coord.dec.degree
                    observable.append(target_data)
            except Exception as e:
                print(f"[BRAIN] Skipping {entry['name']}: {e}")

        # Sort by Altitude (highest first)
        observable.sort(key=lambda x: x['current_alt'], reverse=True)
        
        return {
            "observable": observable,
            "timestamp": now.iso,
            "count": len(observable)
        }

    def get_vsp_data(self, target_name):
        """Optional: Fetch real-time comparison stars from AAVSO API."""
        if not self.api_key: return None
        url = f"https://www.aavso.org/apps/vsp/api/chart/?name={target_name}&format=json"
        try:
            response = requests.get(url)
            return response.json()
        except:
            return None
