#!/usr/bin/env python3
"""
Filename: services/organizer_service.py
Version: 0.7.1
Role: Background service for FITS organization and ASTAP verification.
Owner: Ed de la Rie (PE5ED)
"""

import time
import json
import os
import sys
import tomllib
from pathlib import Path

# Project root for relative imports
project_root = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(project_root))

from core.organizer import FitsOrganizer
from core.astap import AstapResolver

def run_service():
    config_path = project_root / "config.toml"
    status_path = project_root / "logs" / "organizer_status.json"
    status_path.parent.mkdir(parents=True, exist_ok=True)

    # Load config
    try:
        with open(config_path, "rb") as f:
            config = tomllib.load(f)
    except Exception as e:
        print(f"[CRITICAL] Config failure: {e}")
        sys.exit(1)

    # Initialize Cores
    organizer = FitsOrganizer(config)
    resolver = AstapResolver(config)
    scan_interval = config.get("organizer", {}).get("scan_interval", 30)

    print(f"[*] Organizer Service v0.7.1 (ASTAP-Enabled) Active.")

    while True:
        try:
            # 1. Scan and Move
            result = organizer.organize()
            
            # 2. If a file was processed, try to solve the last one
            metrics = result.get("metrics", {})
            last_file_name = metrics.get("last_file")
            
            if last_file_name and last_file_name != "None":
                target_path = organizer.archive_dir / last_file_name
                
                # We only solve if it's actually a FITS file
                if target_path.suffix.lower() in [".fits", ".fit"]:
                    print(f"[*] Verifying alignment for: {last_file_name}")
                    solve_result = resolver.solve(target_path)
                    
                    if solve_result["success"]:
                        result["status"] = "Verified"
                        # We'll attach the solve status to the dashboard metrics
                        result["metrics"]["alignment"] = "OK"
                    else:
                        result["status"] = "Alignment Warn"
                        result["metrics"]["alignment"] = "FAIL"
            
            # 3. Write standardized JSON
            with open(status_path, "w") as f:
                json.dump(result, f)
                
        except Exception as e:
            print(f"[!] Organizer Loop Error: {e}")

        time.sleep(scan_interval)

if __name__ == "__main__":
    run_service()
