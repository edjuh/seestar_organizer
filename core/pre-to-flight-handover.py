#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: core/pre-to-flight-handover.py
Version: 1.2.0 (Pee Pastinakel)
Objective: Evaluates final preflight vitals to authorize the transition to the FLIGHT phase or abort the mission if unsafe.
"""

import json
import os
import sys

PREFLIGHT_DATA = os.path.expanduser("~/seestar_organizer/core/flight/data/preflight_status.json")

def execute_handover():
    print("\n🛡️ === PRE-TO-FLIGHT HANDOVER SEQUENCE ===")
    
    if not os.path.exists(PREFLIGHT_DATA):
        print("❌ ABORT: Preflight vitals data not found. Butler has not completed rounds.")
        sys.exit(1)

    with open(PREFLIGHT_DATA, 'r') as f:
        try:
            vitals = json.load(f)
        except json.JSONDecodeError:
            print("❌ ABORT: Preflight data corrupted.")
            sys.exit(1)

    # The Decision Matrix
    fatal_errors = []

    # 1. Check Bridge
    if vitals.get("bridge") != "OK":
        fatal_errors.append("Alpaca Bridge is offline.")

    # 2. Check GPS (Allow TRYING/Orange, but reject BAD/Red)
    if vitals.get("gps") == "BAD":
        fatal_errors.append("GPS Hardware failure.")

    # 3. Check Weather (Reject Red LEDs: Rain, Storm, Heavy Clouds)
    if vitals.get("weather_led") == "led-red":
        fatal_errors.append(f"Weather conditions unsafe: {vitals.get('weather')}")

    # 4. Check Disk Storage (Reject Red LEDs: <5% space or ERR/Missing)
    if vitals.get("disk_led") == "led-red":
        fatal_errors.append(f"Storage unavailable or critically low: {vitals.get('disk')}")

    # The Verdict
    if fatal_errors:
        print("🚨 HANDOVER DENIED. Mission scrubbed due to the following fatal conditions:")
        for err in fatal_errors:
            print(f"   - {err}")
        print("==========================================\n")
        sys.exit(1)
    else:
        print("✅ HANDOVER APPROVED. All systems nominal.")
        print("🚀 Passing control to the Flight Engine...")
        print("==========================================\n")
        sys.exit(0)

if __name__ == "__main__":
    execute_handover()
