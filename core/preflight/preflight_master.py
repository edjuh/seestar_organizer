#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Seestar Organizer - Pre-Flight Master Conductor
# Path: ~/seestar_organizer/core/preflight/preflight_master.py
# Purpose: The definitive late-afternoon automated conductor.
# ----------------------------------------------------------------

import subprocess
import os
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Conductor")

def run_step(name, script_path):
    logger.info(f"▶️ STARTING: {name}")
    result = subprocess.run([sys.executable, script_path])
    if result.returncode != 0:
        logger.warning(f"⚠️ {name} failed or completed with warnings.")
    else:
        logger.info(f"✅ COMPLETED: {name}")
    return result.returncode

def main():
    base = os.path.expanduser("~/seestar_organizer")
    
    print("\n🥃 CONDUCTOR: Initializing Federation Pre-Flight Sequence...")

    # 1. THE PLANNER: Decides what we shoot based on Haarlem sky
    run_step("NIGHTLY PLANNER", f"{base}/core/preflight/nightly_planner.py")
    
    # 2. THE FETCHER: Secures comp-stars for tonight's 71 targets
    # Note: Fetcher has internal 3.14m (Pi) throttling
    print("⏳ ENRICHMENT: Fetching sequences... (Throttled at 3.14 mins/target)")
    run_step("VSP FETCHER", f"{base}/core/preflight/fetcher.py")
    
    # 3. THE AUDIT: Updates the ACARS Dashboard
    run_step("VITALS AUDIT", f"{base}/core/flight/preflight_check.py")
    
    print("\n🏁 CONDUCTOR: All rounds complete. Systems ready for Handover.")

if __name__ == "__main__":
    main()
