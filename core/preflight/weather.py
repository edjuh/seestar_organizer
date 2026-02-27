#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Seestar Organizer - Predictive Weather Oracle
# Path: ~/seestar_organizer/core/preflight/weather.py
# Purpose: Calculates astronomical dark, fetches Open-Meteo & Buienradar forecasts, and returns a UTF-8 evaluated status.
# ----------------------------------------------------------------

import json
import os
import time
import urllib.request
import urllib.error
import sys
import ephem
from datetime import datetime, timezone

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from core.flight.vault_manager import VaultManager

CACHE_FILE = os.path.expanduser("~/seestar_organizer/core/flight/data/weather_cache.json")
CACHE_EXPIRY = 7200  # 2 hours

class WeatherOracle:
    def __init__(self):
        self.vault = VaultManager()
        self.obs = self.vault.get_observer_config()
        self.lat = float(self.obs.get("lat", 0.0))
        self.lon = float(self.obs.get("lon", 0.0))
        self.elevation = float(self.obs.get("elevation", 0.0))
        self.horizon = str(self.obs.get("sun_altitude_limit", "-18"))
        self.max_cloud = int(self.vault.data.get("Weather", {}).get("MAX_CLOUD_COVER", 50))

    def _get_darkness_window(self):
        """Calculates next Astro Dusk and Dawn in UTC datetime."""
        observer = ephem.Observer()
        observer.lat = str(self.lat)
        observer.lon = str(self.lon)
        observer.elevation = self.elevation
        observer.horizon = self.horizon
        
        try:
            dusk_ephem = observer.next_setting(ephem.Sun(), use_center=True)
            dawn_ephem = observer.next_rising(ephem.Sun(), use_center=True)
            
            dusk_dt = dusk_ephem.datetime().replace(tzinfo=timezone.utc)
            dawn_dt = dawn_ephem.datetime().replace(tzinfo=timezone.utc)
            return dusk_dt, dawn_dt
        except (ephem.AlwaysUpError, ephem.NeverUpError):
            return None, None

    def get_consensus(self):
        """Main evaluation logic with cache."""
        if os.path.exists(CACHE_FILE) and time.time() - os.path.getmtime(CACHE_FILE) < CACHE_EXPIRY:
            try:
                with open(CACHE_FILE, 'r') as f:
                    return json.load(f)
            except Exception:
                pass # Fall through to fetch

        dusk_dt, dawn_dt = self._get_darkness_window()
        
        if not dusk_dt:
            result = {"status": "☀️ DAYLIGHT", "led": "led-red", "details": "Sun does not reach required depth."}
            self._save_cache(result)
            return result

        result = self._evaluate_open_meteo(dusk_dt, dawn_dt)
        self._save_cache(result)
        return result

    def _evaluate_open_meteo(self, dusk_dt, dawn_dt):
        """Fetches hourly data and slices by darkness window."""
        if self.lat == 0.0:
            return {"status": "❓ NO GPS", "led": "led-red", "details": "Cannot fetch weather without coordinates."}
            
        url = f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}&hourly=cloudcover,precipitation,windspeed_10m&timezone=UTC"
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'SeestarOrganizer/1.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                
            hourly = data.get("hourly", {})
            times = hourly.get("time", [])
            clouds = hourly.get("cloudcover", [])
            precip = hourly.get("precipitation", [])
            wind = hourly.get("windspeed_10m", [])
            
            worst_condition = "✨ CLEAR"
            led_status = "led-green"
            
            # Slice the data
            for i, t_str in enumerate(times):
                # Open-Meteo returns 'YYYY-MM-DDTHH:MM'
                dt = datetime.strptime(t_str, "%Y-%m-%dT%H:%M").replace(tzinfo=timezone.utc)
                
                if dusk_dt <= dt <= dawn_dt:
                    # Check conditions in order of severity
                    if precip[i] > 0.0:
                        return {"status": "🌧️ RAIN", "led": "led-red", "details": "Precipitation predicted during dark hours."}
                    elif wind[i] > 40.0: # 40 km/h storm threshold
                        worst_condition = "💨 STORM"
                        led_status = "led-red"
                    elif clouds[i] > self.max_cloud and worst_condition not in ["💨 STORM"]:
                        worst_condition = f"☁️ CLOUDS ({clouds[i]}%)"
                        led_status = "led-red"

            return {"status": worst_condition, "led": led_status, "details": "Forecast evaluated for dark hours."}
            
        except Exception as e:
            return {"status": "⚠️ API ERROR", "led": "led-orange", "details": str(e)}

    def _save_cache(self, result):
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, 'w') as f:
            json.dump(result, f)

if __name__ == "__main__":
    oracle = WeatherOracle()
    print(json.dumps(oracle.get_consensus(), indent=2))
