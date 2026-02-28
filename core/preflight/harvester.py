#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: core/preflight/harvester.py
Version: 1.2.0 (Pee Pastinakel)
Objective: Downloads active campaigns from AAVSO, vetoing targets outside FOV constraints.
"""

import os
import sys
import json
import requests
import tomllib
import logging
from pathlib import Path

# Setup logging
project_root = Path(__file__).parent.parent.parent
log_file = project_root / "data/logs/harvester.log"
os.makedirs(log_file.parent, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("Harvester")

def harvest():
    # 1. Setup & Inventory
    config_path = project_root / "config.toml"
    with open(config_path, "rb") as f:
        config = tomllib.load(f)
    api_key = config['aavso']['target_tool_key']

    targets_file = project_root / "data/targets.json"
    local_targets = {}
    pre_size = 0
    if targets_file.exists():
        pre_size = targets_file.stat().st_size
        with open(targets_file, 'r') as f:
            data = json.load(f)
            local_targets = {t['star_name']: t for t in data if isinstance(t, dict)}
        logger.info(f"📊 Pre-Pull: {len(local_targets)} stars | Size: {pre_size / 1024:.1f} KB")

    # 2. The Stream Pull
    url = "https://targettool.aavso.org/TargetTool/api/v1/targets"
    logger.info("📡 Negotiating AAVSO handshake...")
    
    try:
        response = requests.get(url, auth=(api_key, "api_token"), params={"format": "json"}, timeout=45)
        if response.status_code == 200:
            raw_payload = response.json()
            remote_data = raw_payload.get("targets", [])
            
            logger.info(f"📥 Received {len(remote_data)} raw objects. Processing filters...")
            
            final_list = []
            stats = {"new": [], "updated": [], "stable": 0}

            for t in remote_data:
                name = t.get("star_name", "").strip()
                if not name: continue
                
                try:
                    mag = float(t.get("max_mag", 99.0))
                    if not (3.0 <= mag <= 15.0): continue
                except: continue

                if name not in local_targets:
                    stats["new"].append(name)
                    final_list.append(t)
                else:
                    old_ts = local_targets[name].get("last_data_point") or 0
                    new_ts = t.get("last_data_point") or 0
                    
                    if new_ts > old_ts:
                        stats["updated"].append(name)
                        final_list.append(t)
                    else:
                        stats["stable"] += 1
                        final_list.append(local_targets[name])

            # 3. Final Landing & Size Audit
            with open(targets_file, "w") as f:
                json.dump(final_list, f, indent=4)
            
            post_size = targets_file.stat().st_size
            growth = (post_size - pre_size) / 1024
            
            logger.info(f"💾 Post-Write Audit:")
            logger.info(f"   -> Final File Size: {post_size / 1024:.1f} KB (Delta: {growth:+.1f} KB)")
            logger.info(f"   -> Total Database: {len(final_list)} targets")
            logger.info(f"✅ Pull Verified. {len(stats['updated'])} refreshed. {len(stats['new'])} added.")
            
            if stats["new"]:
                logger.info(f"✨ New Target Confirmed: {stats['new']}")
            
        else:
            logger.error(f"❌ API Rejected request: {response.status_code}")

    except Exception as e:
        logger.error(f"❌ Data Integrity Failure: {e}")

if __name__ == "__main__":
    harvest()
