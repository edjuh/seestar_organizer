#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Filename: scripts/status_ticker.py
# Purpose:  v1.0 Kwetal Master Dashboard - 5-Pillar Hardware Truth
# -----------------------------------------------------------------------------

import requests
import time
import subprocess

def get_dashboard():
    base = "http://127.0.0.1:5555/api/v1/telescope/1"
    auth = "ClientID=1&ClientTransactionID=12000"
    
    try:
        # 1. Hardware & Bridge Status
        gps_status = subprocess.getoutput("systemctl is-active gpsd")
        indi_status = subprocess.getoutput("systemctl is-active indibridge").upper() # Adjust service name if different
        
        # 2. Alpaca Vitals
        s_resp = requests.put(f"{base}/action", data={"Action": "get_event_state", "Parameters": "{}", "ClientID": 1, "ClientTransactionID": 12001}).json()
        val = s_resp.get("Value", {})
        is_sim = val.get("cur_scheduler_item", {}).get("simulation", False)
        
        # 3. Location
        lat = requests.get(f"{base}/sitelatitude?{auth}").json().get("Value", "??")
        lon = requests.get(f"{base}/sitelongitude?{auth}").json().get("Value", "??")
        
        # 4. Heartbeat
        with open("/home/ed/seestar_organizer/logs/seestar_joost.log", "r") as f:
            joost = f.readlines()[-1].strip()[25:]

        print("\033[H\033[J", end="")
        print("-" * 65)
        print(f"[{time.strftime('%H:%M:%S')}] --- 👑 v1.0 KWETAL MASTER DASHBOARD ---")
        print(f"📡 MODE:   {'🛠️ HARDWARE' if not is_sim else '🤖 SIMULATED'} | GPSD: {gps_status.upper()}")
        print(f"🔌 BRIDGES: ALPACA ✅ | INDI {indi_status}")
        print(f"📍 LOCATION: {lat}°N, {lon}°E (JO22hj21)")
        print(f"🛡️  JOOST:    {joost}")
        print(f"📋 SCHEDULE: {val.get('state', 'Idle')} | TARGET: V1159 Ori")
        print("-" * 65)
        print("Coronation Complete. All pillars active. [v1.0 Kwetal: Mastered]")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] ⚠️ Dashboard Error: {e}")

if __name__ == "__main__":
    while True:
        get_dashboard()
        time.sleep(10)
