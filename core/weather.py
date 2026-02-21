import requests
import time
from .env_loader import Config

class WeatherStation:
    def __init__(self):
        self.lat = Config.get("location", "lat") or 52.38
        self.lon = Config.get("location", "lon") or 4.64
        # Fetching current cloud cover and wind speed
        self.url = f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}&current=cloud_cover,wind_speed_10m&forecast_days=1"

    def get_conditions(self):
        """
        Polls Open-Meteo. Returns a dictionary with safety status.
        """
        try:
            r = requests.get(self.url, timeout=5)
            r.raise_for_status()
            data = r.json().get("current", {})
            
            clouds = data.get("cloud_cover", 100)
            wind = data.get("wind_speed_10m", 99)
            
            # Autonomy Logic: Safe if clouds < 20% and wind < 15 km/h
            is_safe = clouds < 20 and wind < 15

            return {
                "safe": is_safe,
                "clouds_pct": clouds,
                "wind_kmh": wind,
                "timestamp": time.time()
            }
        except Exception as e:
            # If the network fails, we assume it is UNSAFE (Fail-Safe)
            return {"safe": False, "error": str(e), "clouds_pct": 100}

# Global Instance
weather_station = WeatherStation()
