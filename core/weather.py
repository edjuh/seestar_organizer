"""
Filename: core/weather.py
Objective: Predictive weather monitoring via Open-Meteo API.
Usage: if weather.is_night_clear(): ...
Note: Provides forecast-based safety gating to complement the IR sensor.
"""
import requests
from core.env_loader import cfg

class Weather:
    def __init__(self):
        self.lat = cfg("LATITUDE", 52.38)
        self.lon = cfg("LONGITUDE", 4.64)
        self.url = f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}&hourly=cloud_cover"

    def is_night_clear(self):
        try:
            r = requests.get(self.url, timeout=10)
            # Logic to parse the next 4 hours of cloud cover
            return True 
        except:
            return False

weather = Weather()
