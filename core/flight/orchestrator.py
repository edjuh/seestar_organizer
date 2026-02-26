#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: core/flight/orchestrator.py
Version: 4.0.0 (The Federation Pilot)
Role: The Pilot
Objective: Executes missions using a standardized API contract.
"""
import os
import json
import time
import logging
from core.flight.sequence_engine import sequence_engine
from api.alpaca_client import AlpacaClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Butler")

def run_orchestrator():
    client = AlpacaClient()
    plan_path = "/home/ed/seestar_organizer/core/flight/data/tonights_plan.json"

    logger.info("Butler: Waking up. Initializing Mission Control.")

    while True:
        if not client.is_connected():
            logger.warning("Butler: Waiting for Alpaca Bridge...")
            time.sleep(10)
            continue

        if not os.path.exists(plan_path):
            logger.error(f"Butler: No flight plan found at {plan_path}")
            time.sleep(60)
            continue

        try:
            with open(plan_path, 'r') as f:
                full_plan = json.load(f)
            
            targets = full_plan.get('targets', [])
            active_plan = sequence_engine.build_night_plan(targets)
            
            if not active_plan:
                logger.info("Butler: No observable targets in window. Standing by.")
                time.sleep(300)
                continue

            logger.info(f"Butler: Engaging {len(active_plan)} targets.")

            for target in active_plan:
                logger.info(f"🚀 [FLIGHT] Mission Start: {target['name']}")
                
                # Using the Clean API: RA/Dec can be floats or strings
                success = client.start_1x1_mosaic(
                    target_name=target['name'],
                    ra=target['ra'],
                    dec=target['dec']
                )
                
                if success:
                    logger.info(f"✅ [FLIGHT] {target['name']} successfully injected into Federation.")
                else:
                    logger.error(f"❌ [FLIGHT] {target['name']} injection failed.")

                # Dwell time for simulator event transition
                time.sleep(30)

        except Exception as e:
            logger.error(f"Butler: Critical Flight Error: {e}")

        logger.info("Butler: Cycle complete. Reviewing plan in 5 minutes.")
        time.sleep(300)

if __name__ == "__main__":
    run_orchestrator()
