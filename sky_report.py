"""
Filename: sky_report.py
Objective: Rapid status report of environmental and hardware readiness.
Usage: python3 sky_report.py
Note: High-level overview of Fog Monitor, GPS lock, and Weather forecast.
"""
from core.fog_monitor import fog_monitor
from core.gps import gps_location
from core.weather import weather

def report():
    print("--- S30-PRO SKY REPORT ---")
    print(f"📍 Location: {gps_location.lat}, {gps_location.lon}")
    print(f"☁️ Sky Clear: {fog_monitor.is_sky_clear()}")
    print(f"🌤️ Forecast: {weather.is_night_clear()}")

if __name__ == "__main__":
    report()
