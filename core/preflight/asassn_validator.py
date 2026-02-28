#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: core/preflight/asassn_validator.py
Version: 1.2.0 (Pee Pastinakel)
Objective: Queries ASAS-SN for current magnitudes to ensure targets are within the S30-Pro's 30mm aperture limits (Mag 7.5 - 13.0).
"""

import os
import json
import urllib.request
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ASAS-SN_Validator")

# S30-Pro Photometric Limits
MAG_LIMIT_FAINT = 13.0  # Aperture limit for 30mm
MAG_LIMIT_BRIGHT = 7.5  # Saturation limit for IMX585

def get_current_mag(star_name):
    """
    Pings ASAS-SN Sky Patrol API.
    Note: In a production environment, use 'pyasassn' or the CSV export.
    This is a robust URL-based fallback.
    """
    clean_name = star_name.replace(' ', '%20')
    url = f"https://asassn.osu.edu/sky-patrol/quiver/search?name={clean_name}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'SeestarOrganizer/1.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            # Sky Patrol returns JSON with the most recent measurements
            data = json.loads(response.read().decode())
            if data and 'mag' in data:
                return float(data['mag'])
    except Exception:
        return None
    return None

def validate_campaign():
    plan_path = os.path.expanduser("~/seestar_organizer/data/campaign_targets.json")
    if not os.path.exists(plan_path):
        logger.error("❌ No campaign file found.")
        return

    with open(plan_path, 'r') as f:
        campaign = json.load(f)

    logger.info(f"Checking ASAS-SN for {len(campaign['targets'])} targets...")

    for target in campaign['targets']:
        name = target.get('name') or target.get('star_name')
        current_mag = get_current_mag(name)
        
        if current_mag is None:
            target['status'] = "UNKNOWN"
            target['reason'] = "No ASAS-SN data"
            continue

        if current_mag > MAG_LIMIT_FAINT:
            target['status'] = "SKIP"
            target['reason'] = f"Too faint ({current_mag})"
        elif current_mag < MAG_LIMIT_BRIGHT:
            target['status'] = "SKIP"
            target['reason'] = f"Too bright ({current_mag})"
        else:
            target['status'] = "READY"
            target['reason'] = f"Mag {current_mag} OK"

    with open(plan_path, 'w') as f:
        json.dump(campaign, f, indent=4)
    
    logger.info("✅ Campaign validated against current sky state.")

if __name__ == "__main__":
    validate_campaign()
