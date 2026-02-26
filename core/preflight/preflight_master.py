#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: core/preflight/preflight_master.py
Version: 1.0.0 (Kwetal)
Role: Preflight Master Guard
Objective: Orchestrates the full Preflight sequence (A-D) to validate the pipeline state.
"""

import subprocess
import sys
import logging
from pathlib import Path

# Setup logging
project_root = Path(__file__).parent.parent.parent
logging.basicConfig(level=logging.INFO, format='%(asctime)s [MASTER] %(message)s')
logger = logging.getLogger("MasterGuard")

def run_step(name, script_path):
    logger.info(f"▶️ Executing {name}...")
    result = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
    if result.returncode == 0:
        logger.info(f"✅ {name} Completed successfully.")
        return True
    else:
        # Print the actual error from the sub-script to the master log
        logger.error(f"❌ {name} Failed:\n{result.stderr}")
        return False

def main():
    preflight_dir = project_root / "core/preflight"
    
    # The Chain of Command (Logic Only)
    steps = [
        ("Harvester (A)", preflight_dir / "harvester.py"),
        ("Fetcher (B)", preflight_dir / "fetcher.py"),
        ("Scheduler (C)", preflight_dir / "nightly_planner.py"),
        ("Audit (D)", preflight_dir / "audit.py")
    ]

    for name, path in steps:
        if not run_step(name, path):
            logger.error("🚫 Preflight sequence aborted due to logic failure.")
            sys.exit(1)

    logger.info("🏆 PREFLIGHT LOGIC VALIDATED. Ready for manual sign-off.")

if __name__ == "__main__":
    main()
