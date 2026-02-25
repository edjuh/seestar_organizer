#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: scripts/dashboard.py
Version: 1.2.0
Role: The Watchdog
Objective: Passive telemetry UI for observing the Alpaca bridge and mission plan.
"""

import time
import sys
import os
import json
import collections

# Add parent directory to path to import api block
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.alpaca_client import AlpacaClient

def get_last_log_line(log_path):
    if not os.path.exists(log_path):
        return "Waiting for Orchestrator..."
    try:
        with open(log_path, "r") as f:
            last_line = collections.deque(f, maxlen=1)[0]
            return last_line.strip()[25:]
    except Exception:
        return "Error reading log..."

def get_plan_summary():
    plan_path = "/home/ed/seestar_organizer/data/tonights_plan.json"
    if not os.path.exists(plan_path):
        return "No plan found."
    try:
        with open(plan_path, "r") as f:
            plan = json.load(f)
            targets = plan.get("targets", [])
            if not targets:
                return "Plan empty."
            next_target = targets[0]["name"]
            return f"{len(targets)} targets queued (Next: {next_target})"
    except Exception:
        return "Error parsing plan."

def run_dashboard():
    client = AlpacaClient()
    log_path = "/home/ed/seestar_organizer/logs/seestar_joost.log"
    true_lat, true_lon = "52.38°N", "4.63°E"
    
    while True:
        is_conn = client.is_connected()
        hw_loc_str = f"{client.get_latitude()}°N, {client.get_longitude()}°E" if is_conn else "OFFLINE"
        
        joost_status = get_last_log_line(log_path)
        plan_status = get_plan_summary()

        print("\033[H\033[J", end="")
        print("-" * 65)
        print(f"[{time.strftime('%H:%M:%S')}] --- 👁️ v1.2 ASTRONOMER'S DASHBOARD ---")
        print(f"🔗 HARDWARE LINK: {'✅ CONNECTED' if is_conn else '❌ DISCONNECTED'}")
        print(f"📍 BRIDGE SAYS:   {hw_loc_str}")
        print(f"🌍 TRUE BASE:     {true_lat}, {true_lon} (Haarlem)")
        print("-" * 65)
        print(f"📋 TONIGHTS PLAN: {plan_status}")
        print(f"🛡️ BUTLER LOG:    {joost_status}")
        print("-" * 65)
        print("Passive monitoring active. Press Ctrl+C to exit.")
        
        time.sleep(5)

if __name__ == "__main__":
    try:
        run_dashboard()
    except KeyboardInterrupt:
        print("\nExiting dashboard.")
