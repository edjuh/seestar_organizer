#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Filename: scripts/status_ticker.py
# Purpose:  v2.2 Kwetal - Alpaca Power Sync & Coronation Watch
# -----------------------------------------------------------------------------

import requests
import time

def ram_the_truth():
    base = "http://127.0.0.1:5555/api/v1/telescope/1"
    try:
        requests.put(f"{base}/sitelatitude", data={"SiteLatitude": 52.37, "ClientID": 1, "ClientTransactionID": 22002}, timeout=2)
        requests.put(f"{base}/sitelongitude", data={"SiteLongitude": 4.64, "ClientID": 1, "ClientTransactionID": 22003}, timeout=2)
    except:
        pass

def get_dashboard():
    base = "http://127.0.0.1:5555/api/v1/telescope/1"
    auth = "ClientID=1&ClientTransactionID=22004"
    
    try:
        # Polling for current state
        r_lat = requests.get(f"{base}/sitelatitude?{auth}", timeout=5).json()
        lat = r_lat.get("Value", "??")
        
        with open("/home/ed/seestar_organizer/logs/seestar_joost.log", "r") as f:
            joost = f.readlines()[-1].strip()[25:]

        print("\033[H\033[J", end="")
        print("-" * 65)
        print(f"[{time.strftime('%H:%M:%S')}] --- ⚡ v2.2 ALPACA POWER DASHBOARD ---")
        print(f"📍 API STATUS: {lat}°N {'✅ HAARLEM' if '52.3' in str(lat) else '❌ GHOST'}")
        print(f"🛡️  JOOST:      {joost}")
        print("-" * 30)
        print(f"📡 MODE:       🛠️ HARDWARE")
        print(f"🔭 TARGETS:    V1159 Ori, M42, M45")
        print("-" * 65)
        print("Ramming truth... [v1.0 Kwetal Stage: Finalized]")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] 🛰️ Bridge is initializing... {e}")

if __name__ == "__main__":
    ram_the_truth() # Use Alpaca Powers on boot!
    while True:
        get_dashboard()
        time.sleep(45)
