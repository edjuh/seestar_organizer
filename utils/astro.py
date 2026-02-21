"""
Pure astronomy utilities — no heavy dependencies.
Used by dashboard, weather, organizer.
"""

import math
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

def calculate_airmass(altitude_deg: float) -> float:
    """Simple but accurate enough airmass for amateur use."""
    if altitude_deg <= 0:
        return 99.0
    return 1.0 / math.sin(math.radians(altitude_deg))

def calculate_maidenhead(lat: float, lon: float) -> str:
    """Convert lat/lon to Maidenhead grid square (6 chars)."""
    if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        return "XX00XX"
    lat += 90
    lon += 180
    a1 = int(lon / 20)
    a2 = int((lon % 20) / 2)
    b1 = int(lat / 10)
    b2 = int((lat % 10) / 0.5)
    c1 = int((lon % 2) * 12)
    c2 = int((lat % 0.5) * 24)
    return f"{chr(65 + a1)}{chr(65 + b1)}{chr(48 + a2)}{chr(48 + b2)}{chr(65 + c1)}{chr(65 + c2)}"

def get_julian_date(dt: datetime = None) -> float:
    """JD at 0h UT."""
    if dt is None:
        dt = datetime.now(timezone.utc)
    dt = dt.replace(tzinfo=ZoneInfo("UTC"))
    year = dt.year
    month = dt.month
    day = dt.day
    if month <= 2:
        year -= 1
        month += 12
    a = year // 100
    b = 2 - a + (a // 4)
    jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + b - 1524.5
    return jd + (dt.hour + dt.minute / 60 + dt.second / 3600) / 24.0

def get_moon_illumination(dt: datetime = None) -> dict:
    """Simple moon phase + illumination (0-100%). Good enough for dashboard."""
    if dt is None:
        dt = datetime.now(timezone.utc)
    jd = get_julian_date(dt)
    days_since_new = jd - 2451549.5
    phase = (days_since_new + 0.5) % 29.53058867
    illumination = (1 - math.cos(2 * math.pi * phase / 29.53058867)) / 2 * 100
    age = phase

    if age < 1.84566:
        phase_name = "New Moon"
    elif age < 5.53699:
        phase_name = "Waxing Crescent"
    elif age < 9.22831:
        phase_name = "First Quarter"
    elif age < 12.91963:
        phase_name = "Waxing Gibbous"
    elif age < 16.61096:
        phase_name = "Full Moon"
    elif age < 20.30228:
        phase_name = "Waning Gibbous"
    elif age < 23.99361:
        phase_name = "Last Quarter"
    else:
        phase_name = "Waning Crescent"

    return {
        "phase": phase_name,
        "illumination_percent": round(illumination, 1),
        "age_days": round(age, 2)
    }
