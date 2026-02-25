#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: core/preflight/fetcher.py
Version: 1.1.5 (Kwetal)
Role: Phase 1.2 - The Sequence Fetcher (The Probe-Proven Method)
"""

import os
import sys
import json
import time
import math
import requests
import tomllib
import logging
from pathlib import Path

# Setup logging
project_root = Path(__file__).parent.parent.parent
log_file = project_root / "data/logs/fetcher.log"
os.makedirs(log_file.parent, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("Fetcher")

def normalize(name):
    return name.lower().replace(" ", "_").replace("+", "p").replace("-", "m")

def get_distance(ra1, dec1, ra2, dec2):
    phi1, phi2 = math.radians(dec1), math.radians(dec2)
    dphi = math.radians(dec2 - dec1)
    dlambda = math.radians(ra2 - ra1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)) * 180 / math.pi

def active_fetch():
    # 1. Load Hardware Specs from TOML
    config_path = project_root / "config.toml"
    try:
        with open(config_path, "rb") as f:
            config = tomllib.load(f)
        delay = config.get('settings', {}).get('fetch_delay', 31.4)
        # We use the probe-proven FOV (180 arcmin = 3 degrees) to ensure the API responds
        api_fov = 180.0 
        mag_limit = 15.0
        safe_radius = config.get('hardware', {}).get('s30_pro', {}).get('telephoto', {}).get('safe_radius', 2.0)
    except Exception as e:
        logger.warning(f"⚠️ Config read failed: {e}. Using Probe defaults.")
        delay, api_fov, mag_limit, safe_radius = 31.4, 180.0, 15.0, 2.0

    targets_path = project_root / "data/targets.json"
    comp_dir = project_root / "data/comp_stars"
    
    with open(targets_path, 'r') as f:
        targets = json.load(f)
    
    existing_normalized = {normalize(f.stem) for f in comp_dir.glob("*.json")}
    missing_targets = [t for t in targets if normalize(t['star_name']) not in existing_normalized]
    
    if not missing_targets:
        logger.info("✅ All targets already synced.")
        return

    logger.info(f"🚀 Fetching {len(missing_targets)} fields via proven Coordinate Method...")

    for i, star in enumerate(missing_targets):
        name = star['star_name']
        ra, dec = star['ra'], star['dec']
        output_path = comp_dir / f"{normalize(name)}.json"
        
        # PROBE-PROVEN PARAMS: Must include FOV and MagLimit even for names
        params = {
            "ra": ra,
            "dec": dec,
            "fov": api_fov,
            "maglimit": mag_limit,
            "format": "json"
        }
        
        logger.info(f"📡 [{i+1}/{len(missing_targets)}] Querying: {name} at ({ra}, {dec})")
        
        try:
            response = requests.get("https://www.aavso.org/apps/vsp/api/chart/", params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                photometry = data.get('photometry', [])
                
                # Check how many comparison stars land in our REAL S30-pro field
                valid_comps = sum(1 for c in photometry if get_distance(ra, dec, float(c.get('ra_deg', 0)), float(c.get('dec_deg', 0))) <= safe_radius)
                
                if valid_comps == 0:
                    logger.warning(f"⚠️ {name}: NO comparison stars found within {safe_radius}° of target.")
                
                with open(output_path, 'w') as f:
                    json.dump(data, f, indent=4)
                
                logger.info(f"✅ Saved. {valid_comps} comps found in field. Sleeping {delay}s...")
                time.sleep(delay)
            else:
                logger.error(f"❌ API Rejected {name} (HTTP {response.status_code}). Msg: {response.text[:100]}")
                time.sleep(5)
                
        except Exception as e:
            logger.error(f"❌ Connection error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    active_fetch()
