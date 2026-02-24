#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Filename: scripts/status_ticker.py
# Purpose:  v2.5 Kwetal - The Relentless Watchdog (Active Reconnection)
# -----------------------------------------------------------------------------

import requests
import time

def enforce_grip(base, auth_data):
    """Actively forces connection and location if the bridge is awake."""
    try:
        # Force Connection
        requests.put(f"{base}/connected", data={**auth_data, "Connected": "True"}, timeout=2)
        time.sleep(1)
        # Force Coordinates
        requests.put(f"{base}/sitelatitude", data={**auth_data, "SiteLatitude": "52.37"}, timeout=2)
        requests.put(f"{base}/sitelongitude", data={**auth_data, "SiteLongitude": "4.64"}, timeout=2)
    except Exception as e:
        pass # If it fails, the bridge is likely still rebooting

def get_dashboard():
    base = "http://127.0.0.1:5555/api/v1/telescope/1"
    auth_data = {"ClientID": 1, "ClientTransactionID": 25000}
    auth_query = "ClientID=1&ClientTransactionID=25001"
    
    try:
        # Check connection status
        r_conn = requests.get(f"{base}/connected?{auth_query}", timeout=2).json()
        is_conn = r_conn.get("Value", False)
        
        # If disconnected, RELENTLESSLY enforce the grip!
        if not is_conn:
            print(f"[{time.strftime('%H:%M:%S')}] ⚠️ DISCONNECTED: Using Alpaca Powers to reconnect...")
            enforce_grip(base, auth_data)
            # Re-check connection after attempting to fix
            is_conn = requests.get(f"{base}/connected?{auth_query}", timeout=2).json().get("Value", False)

        # Pull coordinates
        if is_conn:
            r_lat = requests.get(f"{base}/sitelatitude?{auth_query}", timeout=2).json()
            lat = r_lat.get("Value", "??")
        else:
            lat = "OFFLINE"

        # Read Joost pulse
        with open("/home/ed/seestar_organizer/logs/seestar_joost.log", "r") as f:
            joost = f.readlines()[-1].strip()[25:]

        print("\033[H\033[J", end="")
        print("-" * 65)
        print(f"[{time.strftime('%H:%M:%S')}] --- ⚡ v2.5 RELENTLESS DASHBOARD ---")
        print(f"🔗 CONN STATUS: {'✅ CONNECTED' if is_conn else '❌ DISCONNECTED'}")
        print(f"📍 API LAT:     {lat}°N {'✅ HAARLEM' if str(lat) == '52.37' else '⚠️ WAIT'}")
        print(f"🛡️  JOOST:       {joost}")
        print("-" * 65)
        print("Actively enforcing Hardware Truth... [v1.0 Kwetal]")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] 🛰️ Bridge is knocked out cold... {e}")

if __name__ == "__main__":
    while True:
        get_dashboard()
        time.sleep(15) # Sped up slightly for active recovery
