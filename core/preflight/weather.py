"""
Filename: core/weather.py
Objective: Predictive ensemble weather monitoring (Open-Meteo + Buienradar).
Usage: if weather.is_safe_to_image(): ...
Note: Config-driven safety gating. Fails safely to False if APIs disconnect.
"""
import requests
import os
from datetime import datetime
from core.env_loader import cfg
from core.logger import log_event

class Weather:
    def __init__(self):
        # Pull coordinates from config, default to Haarlem
        self.lat = float(cfg("LATITUDE", 52.38))
        self.lon = float(cfg("LONGITUDE", 4.64))
        
        # Pull dynamic thresholds
        self.max_clouds = float(cfg("MAX_CLOUD_COVER", 40.0))
        self.check_hours = int(cfg("FORECAST_HOURS_AHEAD", 3))
        
        # Simulation Check
        self.simulation_mode = os.getenv("SIMULATION_MODE", "False").lower() == "true"

    def check_open_meteo(self):
        """Returns (is_clear: bool, is_dry: bool) based on Open-Meteo global models."""
        url = f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}&hourly=cloudcover,precipitation&forecast_days=2"
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            data = r.json()
            
            # Get current hour index
            current_hour = datetime.utcnow().hour
            
            # Slice the next X hours from the arrays
            clouds = data['hourly']['cloudcover'][current_hour:current_hour + self.check_hours]
            precip = data['hourly']['precipitation'][current_hour:current_hour + self.check_hours]
            
            avg_clouds = sum(clouds) / len(clouds)
            max_precip = max(precip)
            
            is_clear = avg_clouds <= self.max_clouds
            is_dry = max_precip == 0
            
            log_event(f"Weather [Open-Meteo]: Clouds {avg_clouds}% (Limit: {self.max_clouds}%), Precip {max_precip}mm")
            
            return is_clear, is_dry
            
        except Exception as e:
            log_event(f"Weather [Open-Meteo API Error]: {e}", level="warning")
            return None, None

    def check_buienradar(self):
        """Returns is_dry: bool based on Buienradar's ultra-local rain forecast."""
        url = f"https://gpsgadget.buienradar.nl/data/raintext?lat={self.lat}&lon={self.lon}"
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            
            # Buienradar returns lines of "RRR|HH:mm" where RRR is rain intensity
            lines = r.text.strip().split('\n')
            total_rain = 0
            for line in lines:
                val = int(line.split('|')[0])
                total_rain += val
                
            is_dry = total_rain == 0
            
            if not is_dry:
                log_event("Weather [Buienradar]: Rain detected in the immediate forecast!", level="warning")
            else:
                log_event("Weather [Buienradar]: Clear of rain for the next hour.")
                
            return is_dry
            
        except Exception as e:
            log_event(f"Weather [Buienradar API Error]: {e}", level="warning")
            return None

    def is_safe_to_image(self):
        """
        Ensemble logic check.
        - Simulation Mode Override
        - ANY report of rain = ABORT
        - High clouds = ABORT
        - Network failure = ABORT (Fail-safe)
        """
        if self.simulation_mode:
            log_event("Weather: !!! SIMULATION MODE ACTIVE - FORCING SAFE WEATHER !!!", level="warning")
            return True

        log_event(f"Weather: Polling ensemble APIs for {self.lat}, {self.lon}...")
        
        om_clear, om_dry = self.check_open_meteo()
        br_dry = self.check_buienradar()
        
        # 1. Immediate Rain Override (If either API says it's raining, we close up)
        if om_dry is False or br_dry is False:
            log_event("Weather: PRECIPITATION DETECTED. Unsafe to image.", level="error")
            return False
            
        # 2. Cloud Cover Override
        if om_clear is False:
            log_event("Weather: CLOUD COVER TOO HIGH. Unsafe to image.", level="warning")
            return False
            
        # 3. Fail-Safe (If we have absolutely no data, do not open the scope)
        if om_clear is None and br_dry is None:
            log_event("Weather: ALL APIs UNREACHABLE. Defaulting to UNSAFE.", level="error")
            return False
            
        log_event("Weather: Skies are clear and dry. Safe to image.")
        return True

weather = Weather()
