#!/usr/bin/env python3
"""
Filename: core/utils/observer_math.py
Version: 1.3.0 (Monkel)
Objective: Calculate the 6-character Maidenhead Locator (e.g., JO22hj).
"""

def get_maidenhead_6char(lat, lon):
    if lat is None or lon is None:
        return None

    lon = float(lon) + 180.0
    lat = float(lat) + 90.0

    field_lon = chr(ord('A') + int(lon / 20))
    field_lat = chr(ord('A') + int(lat / 10))

    square_lon = str(int((lon % 20) / 2))
    square_lat = str(int((lat % 10) / 1))

    sub_lon = chr(ord('a') + int((lon % 2) * 12))
    sub_lat = chr(ord('a') + int((lat % 1) * 24))

    return f"{field_lon}{field_lat}{square_lon}{square_lat}{sub_lon}{sub_lat}"
