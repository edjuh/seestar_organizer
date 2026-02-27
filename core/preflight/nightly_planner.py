#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Seestar Organizer - Nightly Planner (Path-Aware)
# Path: ~/seestar_organizer/core/preflight/nightly_planner.py
# Purpose: Scores targets against Haarlem ephemeris and generates tonights_plan.json.
# ----------------------------------------------------------------

import os
import sys
import json
import toml
import ephem
import logging
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("NightlyPlanner")

def load_config():
    path = os.path.expanduser("~/seestar_organizer/config.toml")
    if not os.path.exists(path):
        logger.error("config.toml missing.")
        sys.exit(1)
    with open(path, 'r') as f:
        return toml.load(f)

def get_astronomical_dark(obs, sun_limit):
    """Calculates UTC dusk and dawn for the given sun altitude limit."""
    observer = ephem.Observer()
    observer.lat = str(obs['lat'])
    observer.lon = str(obs['lon'])
    observer.elevation = obs['elevation']
    observer.horizon = str(sun_limit)
    
    try:
        dusk = observer.next_setting(ephem.Sun(), use_center=True)
        dawn = observer.next_rising(ephem.Sun(), use_center=True)
        return dusk, dawn
    except Exception as e:
        logger.error(f"Darkness calculation failed: {e}")
        return None, None

def execute_planning():
    config = load_config()
    loc = config.get('location', {})
    storage = config.get('storage', {})
    hw = config.get('hardware', {})
    planner_cfg = config.get('planner', {})

    # 1. Resolve Dynamic Paths
    target_dir = os.path.expanduser(storage.get('target_dir', '~/seestar_organizer/data'))
    input_file = os.path.join(target_dir, "observable_targets.json")
    output_file = os.path.join(target_dir, "tonights_plan.json")

    if not os.path.exists(input_file):
        logger.error(f"Input file missing: {input_file}")
        return

    # 2. Setup Ephemeris
    sun_limit = planner_cfg.get('sun_altitude_limit', -18.0)
    dusk, dawn = get_astronomical_dark(loc, sun_limit)
    if not dusk: return

    # 3. Process Funnel
    with open(input_file, 'r') as f:
        targets = json.load(f)

    scored_plan = []
    observer = ephem.Observer()
    observer.lat, observer.lon = str(loc['lat']), str(loc['lon'])
    observer.elevation = loc['elevation']
    observer.date = dusk # Start scoring at dusk

    for t in targets:
        star = ephem.FixedBody()
        star._ra = ephem.hours(t['ra'] / 15.0) # RA is in deg in your JSON
        star._dec = ephem.degrees(t['dec'])
        star.compute(observer)

        alt = float(star.alt) * 180.0 / ephem.pi
        
        # Apply the 30-degree science limit
        if alt < loc.get('horizon_limit', 30.0):
            continue

        # Simple Scoring: Priority + Altitude
        score = (1000 if t.get('priority') else 0) + alt
        
        scored_plan.append({
            "name": t['star_name'],
            "ra": t['ra'],
            "dec": t['dec'],
            "exposure_sec": hw.get('default_exposure', 60),
            "frames": 60, # Standard science block
            "alt_at_dusk": round(alt, 2),
            "score": round(score, 1)
        })

    # Sort by score (High to Low)
    scored_plan.sort(key=lambda x: x['score'], reverse=True)

    # 4. Save Final Manifest
    with open(output_file, 'w') as f:
        json.dump(scored_plan, f, indent=4)
    
    logger.info(f"Successfully generated tonights_plan.json with {len(scored_plan)} targets.")

if __name__ == "__main__":
    execute_planning()
