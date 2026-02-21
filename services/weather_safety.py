"""
Filename: services/weather_safety.py
Version: 0.7.1
Role: Background weather monitor service.
"""
import time
import json
import tomllib
from pathlib import Path
from core.weather import WeatherMonitor

def run_safety_monitor():
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)
    
    monitor = WeatherMonitor(config.get("weather", {}))
    status_path = Path("logs/weather_status.json")
    
    print(f"[*] Weather Safety Monitor started for {monitor.location_name}")
    
    while True:
        status = monitor.get_status()
        with open(status_path, "w") as f:
            json.dump(status, f)
        time.sleep(300) # Check every 5 mins

if __name__ == "__main__":
    run_safety_monitor()
