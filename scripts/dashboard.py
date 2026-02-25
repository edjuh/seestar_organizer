#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Filename: scripts/dashboard.py
# Purpose:  Block 3: Passive telemetry UI for observing the Alpaca bridge.
# -----------------------------------------------------------------------------

import time
import sys
import os
import collections

# Add parent directory to path to import api block
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.alpaca_client import AlpacaClient

def get_last_log_line(log_path):
    """Memory-safe way to get the last line of a file using a deque."""
    if not os.path.exists(log_path):
        return "Waiting for Orchestrator..."
    try:
        with open(log_path, "r") as f:
            # collections.deque with maxlen=1 only keeps the very last line in memory
            last_line = collections.deque(f, maxlen=1)[0]
            return last_line.strip()[25:] # Slice off the timestamp
    except Exception:
        return "Error reading log..."

def run_dashboard():
    client = AlpacaClient()
    log_path = "/home/ed/seestar_organizer/logs/seestar_joost.log"
    
    while True:
        # 1. Passive Polling
        is_conn = client.is_connected()
        if is_conn:
            lat = client.get_latitude()
            lon = client.get_longitude()
            loc_str = f"{lat}°N, {lon}°E"
        else:
            loc_str = "OFFLINE"
        
        # 2. Read Joost's Log (safely)
        joost_status = get_last_log_line(log_path)

        # 3. Paint the UI
        print("\033[H\033[J", end="")
        print("-" * 65)
        print(f"[{time.strftime('%H:%M:%S')}] --- 👁️ v1.0 KWETAL DASHBOARD ---")
        print(f"🔗 HARDWARE:   {'✅ CONNECTED' if is_conn else '❌ DISCONNECTED'}")
        print(f"📍 LOCATION:   {loc_str}")
        print(f"🛡️ ORCHESTRATOR: {joost_status}")
        print("-" * 65)
        print("Passive monitoring active. Press Ctrl+C to exit.")
        
        time.sleep(5)

if __name__ == "__main__":
    try:
        run_dashboard()
    except KeyboardInterrupt:
        print("\nExiting dashboard.")
