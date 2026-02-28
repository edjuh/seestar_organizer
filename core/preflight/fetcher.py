#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Objective: Fetches AAVSO data with query-string auth and a file-lock to prevent collisions.
"""
#
# Seestar Organizer - VSP Sequence Fetcher (v2.6)
# Path: ~/seestar_organizer/core/preflight/fetcher.py
# ----------------------------------------------------------------

import os
import json
import time
import urllib.request
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("VSP_Fetcher")

LOCK_FILE = os.path.expanduser("~/.vsp_fetcher.lock")

def acquire_lock():
    if os.path.exists(LOCK_FILE):
        # Check if process is actually running (stale lock check)
        with open(LOCK_FILE, 'r') as f:
            try:
                pid = int(f.read().strip())
                os.kill(pid, 0) # Check if PID exists
                return False
            except (ValueError, OSError):
                os.remove(LOCK_FILE) # Stale lock
    
    with open(LOCK_FILE, 'w') as f:
        f.write(str(os.getpid()))
    return True

def release_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

def load_env():
    env_path = os.path.expanduser("~/seestar_organizer/.env")
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#') and '=' in line:
                    key, val = line.strip().split('=', 1)
                    os.environ[key.strip()] = val.strip().strip('"\'')

def fetch_sequence(star_name):
    api_key = os.environ.get("AAVSO_TARGET_KEY")
    if not api_key:
        logger.error("❌ AAVSO_TARGET_KEY not found!")
        return False

    url = (
        "https://apps.aavso.org/vsp/api/chart/"
        f"?star={star_name.replace(' ', '+')}"
        f"&format=json&fov=60&maglimit=18.0"
        f"&api_key={api_key.strip()}"
    )

    req = urllib.request.Request(url)
    req.add_header("User-Agent", "SeestarOrganizer/2.6 (Contact: ed@S30-pro)")

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
            if not isinstance(data, dict) or "photometry" not in data:
                return False

            normalized = {
                "target": {
                    "star": data.get("star"),
                    "auid": data.get("auid"),
                    "ra_hms": data.get("ra"),
                    "dec_dms": data.get("dec")
                },
                "chart": {
                    "chart_id": data.get("chartid"),
                    "fov_arcmin": data.get("fov"),
                    "maglimit": data.get("maglimit")
                },
                "comparison_stars": data.get("photometry", [])
            }

            seq_dir = os.path.expanduser('~/seestar_organizer/data/comp_stars')
            os.makedirs(seq_dir, exist_ok=True)
            save_path = os.path.join(seq_dir, f"{star_name.lower().replace(' ', '_')}.json")

            with open(save_path, 'w') as f:
                json.dump(normalized, f, indent=4)

            logger.info(f"✅ Secured {len(normalized['comparison_stars'])} comps for {star_name}")
            return True
    except Exception as e:
        logger.error(f"❌ Fetch failed for {star_name}: {e}")
        return False

def run_enrichment():
    if not acquire_lock():
        logger.warning("🛑 Another fetcher is running. Exiting.")
        return

    try:
        load_env()
        target_dir = os.path.expanduser('~/seestar_organizer/data')
        plan_path = os.path.join(target_dir, "campaign_targets.json")
        if not os.path.exists(plan_path): return

        with open(plan_path, 'r') as f:
            campaign = json.load(f)
            
        targets = campaign.get('targets', [])
        seq_dir = os.path.expanduser('~/seestar_organizer/data/comp_stars')

        for entry in targets:
            star = entry.get('star_name') or entry.get('name')
            if not star: continue
            
            if os.path.exists(os.path.join(seq_dir, f"{star.lower().replace(' ', '_')}.json")):
                continue

            if fetch_sequence(star):
                logger.info("Throttling: 31.4s sleep...")
                time.sleep(31.4)
    finally:
        release_lock()

if __name__ == "__main__":
    run_enrichment()
