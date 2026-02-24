#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Filename: scripts/status_ticker.py
# Purpose:  v1.8 Kwetal - Polite Dashboard & Exorcism Monitor
# -----------------------------------------------------------------------------

import requests
import time

def get_dashboard():
    base = "http://127.0.0.1:5555/api/v1/telescope/1"
    auth = "ClientID=1&ClientTransactionID=14000"
    
    try:
        # Check connection first
        r_ping = requests.get(f"{base}/connected?{auth}", timeout=2)
        if r_ping.status_code == 500:
            print(f"[{time.strftime('%H:%M:%S')}] ⚠️ BRIDGE OVERLOAD (500 Error)")
            return

        # Pull Coordinates
        lat = requests.get(f"{base}/sitelatitude?{auth}").json().get("Value", "??")
        lon = requests.get(f"{base}/sitelongitude?{auth}").json().get("Value", "??")
        
        # Mission State
        s_resp = requests.put(f"{base}/action", data={"Action": "get_event_state", "Parameters": "{}", "ClientID": 1, "ClientTransactionID": 14001}).json()
        val = s_resp.get("Value", {})

        print("\033[H\033[J", end="")
        print("-" * 65)
        print(f"[{time.strftime('%H:%M:%S')}] --- 👑 v1.8 POLITE DASHBOARD ---")
        print(f"🛰️  ALPACA:     {'✅ ONLINE' if r_ping.json().get('Value') else '❌ OFFLINE'}")
        print(f"📍 API LOC:    {lat}°N, {lon}°E")
        print(f"⚠️  STATUS:     {'MAASTRICHT DETECTED' if '50.8' in str(lat) else 'HAARLEM STABLE'}")
        print(f"📋 SCHEDULE:   {val.get('state', 'Idle')}")
        print("-" * 65)
        print("Searching for the ghost in the code... [Status: Throttled]")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] 🛰️ Waiting for Specialist... {e}")

if __name__ == "__main__":
    while True:
        get_dashboard()
        time.sleep(30) # Polite 30s interval
