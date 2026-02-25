#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Filename: core/orchestrator.py
# Purpose:  Block 2: The Brain (Joost). Main operational loop and decision maker.
# -----------------------------------------------------------------------------

import time
import sys
import os
import logging

# 1. Setup Logging for the Dashboard to read
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
logger = logging.getLogger("Joost")

# 2. Import Block 1 (The Communicator)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.alpaca_client import AlpacaClient

def run_orchestrator():
    logger.info("Joost: Waking up. Initializing Block 2 Orchestrator.")
    client = AlpacaClient()

    while True:
        logger.info("Joost: Starting routine check...")
        
        # 3. Safely Check Hardware State
        if not client.is_connected():
            logger.warning("Joost: Telescope is offline. Waiting for hardware...")
        else:
            lat = client.get_latitude()
            lon = client.get_longitude()
            logger.info(f"Joost: Telescope online at {lat}°N, {lon}°E. Ready for sequences.")
            # (Future: This is where Joost will read tonights_plan.json and execute slews)
        
        logger.info("Joost: Cycle complete. Sleeping for 60 seconds.")
        time.sleep(60)

if __name__ == "__main__":
    try:
        run_orchestrator()
    except KeyboardInterrupt:
        logger.info("Joost: Orchestrator safely shut down by user.")
