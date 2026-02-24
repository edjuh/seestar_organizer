#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Filename: scripts/status_ticker.py
# Purpose:  The Truth Dashboard (v1.4 Kwetal) - Hardware vs Sim Detection
# -----------------------------------------------------------------------------

import requests
import time
import os

def get_dashboard():
    base = "http://127.0.0.1:5555/api/v1/telescope/1"
    auth = "ClientID=1&ClientTransactionID=7001"
    
    try:
        # 1. Get State to check for Simulation flags
        s_resp = requests.put(f"{base}/action", data={"Action": "get_event_state", "Parameters": "{}", "ClientID": 1, "ClientTransactionID": 7002}).json()
        val = s_resp.get("Value", {})
        
        # Check if the bridge thinks it is in simulation
        # In your log: 'simulation': True, 'is_debug': True
        is_sim = val.get("cur_scheduler_item", {}).get("simulation", True)
        mode_tag = "🛠️ HARDWARE" if not is_sim else "🤖 SIMULATED"

        # 2. Coordinates
        lat = requests.get(f"{base}/sitelatitude?{auth}").json().get("Value", "??")
        lon = requests.get(f"{base}/sitelongitude?{auth}").json().get("Value", "??")
        
        # 3. Joost Pulse
        with open("/home/ed/seestar_organizer/logs/seestar_joost.log", "r") as f:
            joost = f.readlines()[-1].strip()[25:]

        print("\033[H\033[J", end="")
        print("-" * 65)
        print(f"[{time.strftime('%H:%M:%S')}] --- 🌟 THE TRUTH DASHBOARD (v1.4) ---")
        print(f"📡 MODE:       {mode_tag}")
        print(f"📍 LOCATION:   {lat}°N, {lon}°E (JO22hj21)")
        print(f"🛡️  JOOST:      {joost}")
        print(f"📋 SCHEDULE:   {val.get('state', 'Idle')}")
        print("-" * 65)
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] ⚠️ Dashboard Error: {e}")

if __name__ == "__main__":
    while True:
        get_dashboard()
        time.sleep(10)
