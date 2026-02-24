#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Filename: scripts/status_ticker.py
# Purpose:  v1.0 Kwetal Coronation Dashboard - Manual Reading Mode
# -----------------------------------------------------------------------------

import requests
import time
import subprocess

def get_dashboard():
    base = "http://127.0.0.1:5555/api/v1/telescope/1"
    auth = "ClientID=1&ClientTransactionID=10000"
    
    try:
        # 1. Hardware Check
        gps_status = subprocess.getoutput("systemctl is-active gpsd")
        
        # 2. Alpaca Status & Sim Detection
        s_resp = requests.put(f"{base}/action", data={"Action": "get_event_state", "Parameters": "{}", "ClientID": 1, "ClientTransactionID": 10001}).json()
        val = s_resp.get("Value", {})
        
        # Checking simulation state from the bridge response
        is_sim = val.get("cur_scheduler_item", {}).get("simulation", True)
        mode_tag = "🛠️ HARDWARE" if not is_sim else "🤖 SIMULATED"

        # 3. Location & Targets
        lat = requests.get(f"{base}/sitelatitude?{auth}").json().get("Value", "??")
        lon = requests.get(f"{base}/sitelongitude?{auth}").json().get("Value", "??")
        
        # 4. Joost Heartbeat
        with open("/home/ed/seestar_organizer/logs/seestar_joost.log", "r") as f:
            joost = f.readlines()[-1].strip()[25:]

        print("\033[H\033[J", end="")
        print("-" * 65)
        print(f"[{time.strftime('%H:%M:%S')}] --- 👑 v1.0 KWETAL CORONATION DASHBOARD ---")
        print(f"📡 MODE:       {mode_tag} | GPSD: {gps_status.upper()}")
        print(f"📍 LOCATION:   {lat}°N, {lon}°E (JO22hj21)")
        print(f"🛡️  JOOST:      {joost}")
        print(f"📋 SCHEDULE:   {val.get('state', 'Idle')}")
        print(f"🔭 TOP TARGETS: V1159 Ori, M42, M45")
        print("-" * 65)
        print("Reading manuals... [Status: Analyzing Simulation Flags]")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] ⚠️ Dashboard Error: {e}")

if __name__ == "__main__":
    while True:
        get_dashboard()
        time.sleep(10)
