#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Filename: scripts/status_ticker.py
# Purpose:  Maidenhead Reality Dashboard (v1.5 Kwetal) - GPSD & Truth Detection
# -----------------------------------------------------------------------------

import requests
import time
import subprocess

def get_dashboard():
    base = "http://127.0.0.1:5555/api/v1/telescope/1"
    auth = "ClientID=1&ClientTransactionID=8001"
    
    try:
        # 1. Check GPSD Service Status
        gps_status = subprocess.getoutput("systemctl is-active gpsd")
        
        # 2. Pull Alpaca Vitals
        s_resp = requests.put(f"{base}/action", data={"Action": "get_event_state", "Parameters": "{}", "ClientID": 1, "ClientTransactionID": 8002}).json()
        val = s_resp.get("Value", {})
        
        # 3. Pull Coordinates and Force Refresh
        lat = requests.get(f"{base}/sitelatitude?{auth}").json().get("Value", "??")
        lon = requests.get(f"{base}/sitelongitude?{auth}").json().get("Value", "??")
        
        # 4. Joost Heartbeat
        with open("/home/ed/seestar_organizer/logs/seestar_joost.log", "r") as f:
            joost = f.readlines()[-1].strip()[25:]

        print("\033[H\033[J", end="")
        print("-" * 65)
        print(f"[{time.strftime('%H:%M:%S')}] --- 📍 MAIDENHEAD REALITY (v1.5) ---")
        print(f"🛰️  GPSD:       {gps_status.upper()} (/dev/ttyACM0)")
        print(f"📍 LOCATION:   {lat}°N, {lon}°E")
        print(f"🛡️  JOOST:      {joost}")
        print(f"📋 SCHEDULE:   {val.get('state', 'Idle')}")
        print("-" * 65)
        print("Flipping simulation switch... [v1.0 Kwetal Stage: Finalizing]")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] ⚠️ Dashboard Error: {e}")

if __name__ == "__main__":
    while True:
        get_dashboard()
        time.sleep(10)
EOF
