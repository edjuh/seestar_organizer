#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Seestar Organizer - VSP Sequence Fetcher
# Path: ~/seestar_organizer/core/preflight/fetcher.py
# Purpose: Secures AAVSO comparison star sequences for the nightly plan.
# ----------------------------------------------------------------

import os
import sys
import json
import time
import toml
import urllib.request
import base64
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("VSP_Fetcher")

def load_config():
    path = os.path.expanduser("~/seestar_organizer/config.toml")
    with open(path, 'r') as f:
        return toml.load(f)

def fetch_sequence(star_name, config):
    """Hits AAVSO VSP API for a specific target."""
    aavso = config.get('aavso', {})
    storage = config.get('storage', {})
    
    # API Params from api_protocol.md
    api_key = aavso.get('target_key') # The AAVSO_TARGET_KEY
    url = f"https://app.aavso.org/vsp/api/chart/?star={star_name.replace(' ', '+')}&format=json&fov=60&maglimit=18.0"
    
    # Auth: Basic (Username: key, Password: api_token)
    auth_str = f"{api_key}:api_token"
    encoded_auth = base64.b64encode(auth_str.encode()).decode()

    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Basic {encoded_auth}")
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
            
            # Save to the authoritative sequence directory
            seq_dir = os.path.expanduser(storage.get('sequence_dir', '~/seestar_organizer/data/sequences'))
            os.makedirs(seq_dir, exist_ok=True)
            
            filename = f"{star_name.lower().replace(' ', '_')}.json"
            save_path = os.path.join(seq_dir, filename)
            
            with open(save_path, 'w') as f:
                json.dump(data, f, indent=4)
            
            logger.info(f"✅ Secured sequence for {star_name}")
            return True
    except Exception as e:
        logger.error(f"❌ Failed to fetch {star_name}: {e}")
        return False

def run_enrichment():
    config = load_config()
    storage = config.get('storage', {})
    target_dir = os.path.expanduser(storage.get('target_dir', '~/seestar_organizer/data'))
    seq_dir = os.path.expanduser(storage.get('sequence_dir', '~/seestar_organizer/data/sequences'))
    plan_path = os.path.join(target_dir, "tonights_plan.json")

    if not os.path.exists(plan_path):
        logger.error("No nightly plan found. Run the planner first.")
        return

    with open(plan_path, 'r') as f:
        plan = json.load(f)

    logger.info(f"Starting enrichment for {len(plan)} targets...")
    
    for entry in plan:
        star = entry['name']
        filename = f"{star.lower().replace(' ', '_')}.json"
        
        if os.path.exists(os.path.join(seq_dir, filename)):
            continue # Already have it
            
        logger.info(f"Targeting: {star}...")
        success = fetch_sequence(star, config)
        
        if success:
            # Mandatory throttling from api_protocol.md
            logger.info("Respecting VSP Throttling: 188.4s sleep...")
            time.sleep(188.4)  # Pi-Minutes Throttling

if __name__ == "__main__":
    run_enrichment()
