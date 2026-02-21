import threading
import time
import requests
from .env_loader import cfg

class WeatherSensor:
    def __init__(self):
        self.state = {
            "safe": False,
            "clouds_pct": 100,
            "wind_kmh": 99,
            "timestamp": 0,
            "error": "Initializing"
        }
        self._lock = threading.Lock()
        
        # Load logic limits from config.toml
        self.lat = cfg("location", "lat", 52.38)
        self.lon = cfg("location", "lon", 4.64)
        self.max_clouds = cfg("autonomy", "max_clouds_pct", 20.0)
        self.max_wind = cfg("autonomy", "max_wind_kmh", 15.0)
        
        self.url = f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}&current=cloud_cover,wind_speed_10m"
        
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        while True:
            try:
                r = requests.get(self.url, timeout=10)
                if r.status_code == 200:
                    data = r.json().get("current", {})
                    clouds = data.get("cloud_cover", 100)
                    wind = data.get("wind_speed_10m", 99)
                    
                    is_safe = (clouds <= self.max_clouds) and (wind <= self.max_wind)
                    
                    with self._lock:
                        self.state.update({
                            "safe": is_safe,
                            "clouds_pct": clouds,
                            "wind_kmh": wind,
                            "timestamp": time.time(),
                            "error": None
                        })
                else:
                    with self._lock:
                        self.state.update({"safe": False, "error": f"HTTP {r.status_code}"})
            except Exception as e:
                with self._lock:
                    self.state.update({"safe": False, "error": str(e)})
            
            # Sleep for 5 minutes before polling again (Open-Meteo updates hourly anyway)
            time.sleep(300)

    def get_state(self):
        """Thread-safe instant read for the Dashboard."""
        with self._lock:
            return self.state.copy()

# Singleton instance
weather_station = WeatherSensor()
