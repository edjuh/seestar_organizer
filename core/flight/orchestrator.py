#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: core/orchestrator.py
Version: 1.1.0
Role: The Butler & Safety Gate
Objective: Main operational loop. Enforces hardware safety before executing sequence targets.
"""

import time
import sys
import os
import json
import logging

# Setup Logging for the Dashboard to read
LOG_DIR = "/home/ed/seestar_organizer/logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "seestar_joost.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
# The Butler assumes his proper title
logger = logging.getLogger("Butler")

# Import Local Modules (Block 1 + Core Logic)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.alpaca_client import AlpacaClient

# Gracefully import environmental monitors
try:
    from core from core.preflight import weather
    from core from core.preflight import fog_monitor
except ImportError as e:
    logger.warning(f"Butler: Could not load environmental modules: {e}")
    weather = None
    fog_monitor = None

def load_tonights_plan():
    """Reads the JSON plan prepared by the nightly_planner."""
    plan_path = "/home/ed/seestar_organizer/core/flight/data/tonights_plan.json"
    if not os.path.exists(plan_path):
        return None
    try:
        with open(plan_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Butler: Error reading tonight's plan: {e}")
        return None

def run_orchestrator():
    logger.info("Butler: Waking up. Initializing Block 2 Orchestrator.")
    client = AlpacaClient()

    while True:
        logger.info("Butler: Starting Safety Gate evaluation...")
        
        # --- 1. THE SAFETY GATE ---
        is_weather_safe = weather.is_safe() if hasattr(weather, 'is_safe') else True
        is_fog_clear = fog_monitor.is_clear() if hasattr(fog_monitor, 'is_clear') else True
        
        if not is_weather_safe or not is_fog_clear:
            logger.warning("Butler: Weather/Fog is UNSAFE. Aborting ops. Sleeping 10m.")
            time.sleep(600)  # 10 minutes
            continue

        # --- 2. THE HARDWARE CHECK ---
        if not client.is_connected():
            logger.warning("Butler: Telescope is offline. Waiting for hardware...")
            time.sleep(60)
            continue
            
        lat = client.get_latitude()
        logger.info(f"Butler: Hardware verified online at {lat}°N.")

        # --- 3. THE EXECUTION ---
        plan = load_tonights_plan()
        if not plan:
            logger.info("Butler: No valid targets found in tonights_plan.json. Sleeping 5m.")
            time.sleep(300)
            continue
            
        logger.info(f"Butler: Plan loaded. Engaging {len(plan.get('targets', []))} targets...")
        # (Future: Loop through plan['targets'], format the 1x1 Mosaic trick, and send to client)
        
        logger.info("Butler: Cycle complete. Sleeping for 5 minutes.")
        time.sleep(300)

if __name__ == "__main__":
    try:
        run_orchestrator()
    except KeyboardInterrupt:
        logger.info("Butler: Orchestrator safely shut down by user.")
