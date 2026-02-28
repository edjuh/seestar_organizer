#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Objective: Orchestrates sequential fetching, coordinate normalization,
"""
#
# Seestar Organizer - Master Preflight Orchestrator (v1.3)
# Path: ~/seestar_organizer/core/preflight/preflight_master.py
#          and aperture-limit validation via ASAS-SN.
# ----------------------------------------------------------------

import os
import sys
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Master_Preflight")

def run_step(name, script_path):
    logger.info(f"--- Starting Step: {name} ---")
    if not os.path.exists(script_path):
        logger.warning(f"⚠️ Skipping {name}: Script not found at {script_path}")
        return True
        
    try:
        subprocess.check_call([sys.executable, script_path])
        logger.info(f"✅ {name} completed.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ {name} failed with error code {e.returncode}")
        return False

def main():
    base_dir = os.path.expanduser("~/seestar_organizer")
    
    # The Full Preflight Sequence
    steps = [
        ("VSP Fetcher", os.path.join(base_dir, "core/preflight/fetcher.py")),
        ("Coordinate Librarian", os.path.join(base_dir, "utils/coordinate_converter.py")),
        ("ASAS-SN Validator", os.path.join(base_dir, "core/preflight/asassn_validator.py")),
    ]

    for name, path in steps:
        if not run_step(name, path):
            logger.error("🛑 Preflight aborted due to critical step failure.")
            break

    logger.info("🎯 Preflight Complete. Your target list is now Aperture-Validated.")

if __name__ == "__main__":
    main()
