#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Filename: scripts/status_ticker.py
# Purpose:  v1.7 Kwetal - Discrepancy Hunter & GPS Force
# -----------------------------------------------------------------------------

import requests
import time

def get_dashboard():
    base = "http://127.0.0.1:5555/api/v1/telescope/1"
    auth = "ClientID=1&ClientTransactionID=13000"
    
    try:
        # 1. FORCE HAARLEM (JO22hj21) ON EVERY TICK
        requests.put(f"{base}/sitelatitude", data={"SiteLatitude": 52.37, "ClientID": 1, "ClientTransactionID": 13001})
        requests.put(f"{base}/sitelongitude", data={"SiteLongitude": 4.64, "ClientID": 1, "ClientTransactionID": 13002})
        
        # 2. Alpaca Vitals
        s_resp = requests.put(f"{base}/action", data={"Action": "get_event_state", "Parameters": "{}", "ClientID": 1, "ClientTransactionID": 13003}).json()
        val = s_resp.get("Value", {})
        
        # 3. Read Current (Possibly Haunted) Coordinates
        lat = requests.get(f"{base}/sitelatitude?{auth}").json().get("Value", "??")
        lon = requests.get(f"{base}/sitelongitude?{auth}").json().get("Value", "??")
        
        # 4. Heartbeat
        with open("/home/ed/seestar_organizer/logs/seestar_joost.log", "r") as f:
            joost = f.readlines()[-1].strip()[25:]

        print("\033[H\033[J", end="")
        print("-" * 65)
        print(f"[{time.strftime('%H:%M:%S')}] --- 👻 GHOST HUNTER DASHBOARD (v1.7) ---")
        print(f"📍 TRUTH:      JO22hj21 (Haarlem)")
        print(f"📍 API LAT:    {lat}°N {'⚠️ MAASTRICHT ERROR' if '50.8' in str(lat) else '✅'}")
        print(f"📍 API LON:    {lon}°E {'⚠️ MAASTRICHT ERROR' if '5.6' in str(lon) else '✅'}")
        print(f"🛡️  JOOST:      {joost}")
        print(f"📋 SCHEDULE:   {val.get('state', 'Idle')}")
        print("-" * 65)
        print("Ramming the Haarlem coordinates into the API... [Status: Exorcising]")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] ⚠️ Dashboard Error: {e}")

if __name__ == "__main__":
    while True:
        get_dashboard()
        time.sleep(10)
