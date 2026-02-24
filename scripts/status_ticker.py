#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Filename: scripts/status_ticker.py
# Purpose:  The Coronation Dashboard (v1.6 Kwetal) - Target Specialist & Truth
# -----------------------------------------------------------------------------

import requests
import time
import subprocess

def get_dashboard():
    base = "http://127.0.0.1:5555/api/v1/telescope/1"
    auth = "ClientID=1&ClientTransactionID=9000"
    
    try:
        # 1. Hardware & System Check
        gps_status = subprocess.getoutput("systemctl is-active gpsd")
        
        # 2. Alpaca Vitals & Simulation Detection
        s_resp = requests.put(f"{base}/action", data={"Action": "get_event_state", "Parameters": "{}", "ClientID": 1, "ClientTransactionID": 9001}).json()
        val = s_resp.get("Value", {})
        
        # The 'simulation' flag is often nested in the device config or event state
        is_sim = val.get("cur_scheduler_item", {}).get("simulation", True)
        mode_tag = "🛠️ HARDWARE" if not is_sim else "🤖 SIMULATED"

        # 3. Location & Targets (Corrected for Haarlem JO22hj21)
        lat = requests.get(f"{base}/sitelatitude?{auth}").json().get("Value", "??")
        lon = requests.get(f"{base}/sitelongitude?{auth}").json().get("Value", "??")
        
        # Target Specialist: High Altitude Targets for Haarlem right now
        # 
        top_targets = ["V1159 Ori (Zenith-ish)", "M42 (Prime)", "M45 (Setting)"]

        # 4. Joost Heartbeat
        with open("/home/ed/seestar_organizer/logs/seestar_joost.log", "r") as f:
            joost = f.readlines()[-1].strip()[25:]

        print("\033[H\033[J", end="")
        print("-" * 65)
        print(f"[{time.strftime('%H:%M:%S')}] --- 👑 v1.6 CORONATION DASHBOARD ---")
        print(f"📡 MODE:       {mode_tag} | GPSD: {gps_status.upper()}")
        print(f"📍 LOCATION:   {lat}°N, {lon}°E (JO22hj21)")
        print(f"🛡️  JOOST:      {joost}")
        print(f"📋 SCHEDULE:   {val.get('state', 'Idle')} (Item {val.get('item_number', 'N/A')})")
        print(f"🔭 TOP 3:      {', '.join(top_targets)}")
        print("-" * 65)
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] ⚠️ Dashboard Error: {e}")

if __name__ == "__main__":
    while True:
        get_dashboard()
        time.sleep(10)
