#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Filename: scripts/status_ticker.py
# Purpose:  v2.0 Kwetal - The Investigator Dashboard (Polite Mode)
# -----------------------------------------------------------------------------

import requests
import time
import os

def get_dashboard():
    base = "http://127.0.0.1:5555/api/v1/telescope/1"
    auth = "ClientID=1&ClientTransactionID=20000"
    
    try:
        # Polling with a longer timeout to be polite to the bridge
        r_lat = requests.get(f"{base}/sitelatitude?{auth}", timeout=5).json()
        lat = r_lat.get("Value", "??")
        
        # Checking for the Maastricht Ghost
        is_maastricht = "50.8" in str(lat)
        
        # Check if suspect files exist
        csc_exists = os.path.exists("/home/ed/seestar_alp/front/csc_sites.json")
        
        print("\033[H\033[J", end="")
        print("-" * 65)
        print(f"[{time.strftime('%H:%M:%S')}] --- 🕵️ v2.0 THE INVESTIGATOR DASHBOARD ---")
        print(f"📍 CURRENT API LAT: {lat}°N")
        print(f"👻 GHOST STATUS:    {'⚠️ MAASTRICHT DETECTED' if is_maastricht else '✅ HAARLEM STABLE'}")
        print("-" * 30)
        print(f"📂 CSC_SITES.JSON:  {'FOUND' if csc_exists else 'MISSING'}")
        print(f"📂 EPHEM/CITIES:    CHECKING...")
        print("-" * 65)
        print("Interrogating library files... [Status: Forensic Analysis]")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] 🛰️ Bridge is resting... {e}")

if __name__ == "__main__":
    while True:
        get_dashboard()
        time.sleep(45) # Very polite polling to allow the bridge to recover
