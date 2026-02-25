#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: core/preflight/preflight_master.py
Version: 1.0.0 (Kwetal)
Role: Preflight Master Guard
Objective: Orchestrates the full Preflight sequence and validates the pipeline state.
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
        logger.error(f"❌ {name} Failed: {result.stderr}")
        return False

def main():
    preflight_dir = project_root / "core/preflight"
    
    # The Chain of Command
    steps = [
        ("Harvester (A)", preflight_dir / "harvester.py"),
        ("Fetcher (B)", preflight_dir / "fetcher.py"),
        ("Scheduler (C)", preflight_dir / "nightly_planner.py"),
        ("Audit (D)", preflight_dir / "audit.py")
    ]

    for name, path in steps:
        if not run_step(name, path):
            logger.error("🚫 Preflight sequence aborted due to failure.")
            sys.exit(1)

    # Final Handshake: Manifest & Git
    logger.info("📦 Finalizing Preflight: Updating Manifest and Git...")
    try:
        # Generate Manifest
        manifest_gen = project_root / "utils/generate_manifest.py"
        with open(project_root / "FILE_MANIFEST.md", "w") as f:
            subprocess.run([sys.executable, str(manifest_gen)], stdout=f)
        
        # Git Push
        subprocess.run(["git", "add", "."], cwd=project_root)
        subprocess.run(["git", "commit", "-m", "v1.0 Kwetal: Preflight Full Chain Validated."], cwd=project_root)
        subprocess.run(["git", "push"], cwd=project_root)
        
        logger.info("🏆 PREFLIGHT COMPLETE. The system is ready for Flight.")
        
    except Exception as e:
        logger.error(f"❌ Failed to seal Preflight: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
