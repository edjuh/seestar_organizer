"""
Filename: utils/weather_safety.py
Version: 0.9.8
"""
import requests
import logging
from datetime import datetime, timezone

logger = logging.getLogger("WeatherSafety")

class WeatherSafety:
    def __init__(self, lat=52.38, lon=4.64):
        self.url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=cloud_cover,precipitation_probability&timezone=UTC"
        self._cache = None
        self._last_fetch = None

    def check(self):
        now_utc = datetime.now(timezone.utc)
        
        if self._last_fetch and (now_utc - self._last_fetch).seconds < 600: # Increase cache to 10 mins
            return self._cache

        try:
            # Increase timeout to 20s for slow satellite/Stellarmate links
            r = requests.get(self.url, timeout=20)
            r.raise_for_status()
            data = r.json().get("hourly", {})
            
            times = data.get("time", [])
            now_str = now_utc.strftime("%Y-%m-%dT%H:00")
            
            try:
                idx = next(i for i, t in enumerate(times) if t == now_str)
            except StopIteration:
                idx = 0 

            clouds = (data.get("cloud_cover") or [100])[idx]
            precip = (data.get("precipitation_probability") or [100])[idx]
            is_safe = (clouds < 80) and (precip < 5)

            status = {
                "safe": is_safe,
                "metrics": {"clouds": clouds, "precip": precip},
                "timestamp": now_str,
                "status_msg": "NOMINAL" if is_safe else "UNSAFE CONDITIONS"
            }
            
            self._cache = status
            self._last_fetch = now_utc
            return status

        except Exception as e:
            logger.error(f"Weather Logic Failure: {e}")
            # If we have a cache, use it even if it's old rather than failing
            if self._cache:
                return self._cache
            return {
                "safe": False, 
                "metrics": {"clouds": 100, "precip": 100},
                "status_msg": "STALE/ERROR"
            }
