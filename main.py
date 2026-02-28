#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: main.py
Version: 1.2.0 (Garmt)
Objective: Primary entry point for the Seestar Sentry daemon; orchestrates the "Williamina" and "Annie" hardware loops with path-aware imports.
"""

import time
import os
import sys

# Standardize the environment path so root can see the "Pillars"
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(project_root, 'core'))

from core.preflight.weather import weather
from core.preflight.ephemeris import observer
from core.selector import selector
from api.alpaca_client import alpaca
from core.logger import log_event

def verify_inventory():
    """Check if we have targets to work with before starting."""
    vault_path = os.path.join(project_root, "data/sequences/")
    if not os.path.exists(vault_path):
        log_event(f"CRITICAL: Vault path {vault_path} missing!", level="error")
        return 0
    
    count = len([f for f in os.listdir(vault_path) if f.endswith('.json')])
    log_event(f"Inventory: Found {count} object JSONs in vault.")
    return count

def run_cycle():
    sim_mode = os.getenv("SIMULATION_MODE", "False").lower() == "true"
    dark_mode = os.getenv("DARKNESS_OVERRIDE", "False").lower() == "true"
    
    log_event(f"Kwetal: Cycle start (Sim: {sim_mode}, Dark: {dark_mode})")

    if not sim_mode and not weather.is_safe_to_image():
        log_event("Kwetal: Weather UNSAFE. Commanding Lockdown.")
        alpaca.park_telescope()
        return

    is_dark = observer.is_dark_enough()
    if not (sim_mode or dark_mode or is_dark):
        log_event(f"Kwetal: Sun is at {observer.sun_alt:.1f}°. Waiting for darkness.")
        return 

    plan = selector.get_night_plan()
    if plan:
        target = plan
        log_event(f"Kwetal: Selected priority target {target['display_name']} at {target['alt']:.1f}°.")
        alpaca.start_observation(target)
    else:
        log_event("Kwetal: No valid targets found in current sky window.")

def main():
    log_event("Kwetal Sentry: Initializing Garmt v1.2.0...")
    if verify_inventory() == 0:
        log_event("CRITICAL: No targets found. Exiting.", level="error")
        sys.exit(1)

    while True:
        try:
            run_cycle()
        except Exception as e:
            log_event(f"Kwetal: Runtime Error: {e}", level="error")
        time.sleep(600)

if __name__ == "__main__":
    main()
