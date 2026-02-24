!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Filename: scripts/status_ticker.py
# Purpose:  Authenticated Watchdog & Mission Telemetry (v1.0 Kwetal)
# Author:   Ed (The Specialist) & Gemini
# Version:  v1.0
# -----------------------------------------------------------------------------

import requests
import time
import sys

def watchdog_ticker():
    """Patrols the Alpaca connection and monitors mission state."""
    base = "http://127.0.0.1:5555/api/v1/telescope/1"
    auth = "ClientID=1&ClientTransactionID=2700"
    
    while True:
        try:
            # 1. Check Connection via Alpaca Property
            r = requests.get(f"{base}/connected?{auth}", timeout=2)
            is_conn = r.json().get("Value", False)
            
            # 2. Force Reconnect if Flapped
            if not is_conn:
                requests.put(f"{base}/connected", data={"Connected": "true", "ClientID": 1, "ClientTransactionID": 2701})
            
            # 3. Pull Mission State via authenticated Action
            s = requests.put(f"{base}/action", data={
                "Action": "get_event_state", 
                "Parameters": "{}", 
                "ClientID": 1, 
                "ClientTransactionID": 2702
            })
            val = s.json().get("Value", {})
            state = val.get("state", "Idle")
            item = val.get("item_number", "N/A")
            stacking = "🔭 Imaging" if val.get("is_stacking") else "⏳ Waiting"
            
            # 4. Pull Joost Heartbeat
            with open("/home/ed/seestar_organizer/logs/seestar_joost.log", "r") as f:
                joost_msg = f.readlines()[-1].strip()[25:]

            # The 'Heer van Stand' Console Output
            print(f"[{time.strftime('%H:%M:%S')}] Conn: {'✅' if is_conn else '❌'} | {state} ({item}) | {stacking} | Joost: {joost_msg}")
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] 🛰️ Bridge search... {e}")
        
        time.sleep(30)

if __name__ == "__main__":
    print("--- 🔭 Williamina v1.0 Kwetal Watchdog Active ---")
    watchdog_ticker()
