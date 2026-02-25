#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: core/nightly_planner.py
Version: 1.1.0
Role: The Astronomer
Objective: Filter the AAVSO target library for visibility from Haarlem tonight.
"""

import os
import json
import ephem
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger("NightlyPlanner")

# 1. Haarlem Parameters
HAARLEM_LAT = '52.38'
HAARLEM_LON = '4.63'
ALTITUDE_LIMIT = 30.0 # Degrees above horizon

def get_haarlem_observer():
    obs = ephem.Observer()
    obs.lat = HAARLEM_LAT
    obs.lon = HAARLEM_LON
    obs.elevation = 0
    # Set to current UTC time
    obs.date = datetime.utcnow()
    return obs

def ensure_dummy_library(targets_file):
    """Creates a dummy AAVSO library if you don't have one yet."""
    if not os.path.exists(targets_file):
        dummy_data = [
            {"name": "V1159 Ori", "ra": "05:32:00", "dec": "-05:54:00", "exposure": 10, "count": 180},
            {"name": "CH Cyg",    "ra": "19:24:33", "dec": "50:14:29",  "exposure": 10, "count": 180},
            {"name": "SS Cyg",    "ra": "21:42:42", "dec": "43:35:09",  "exposure": 10, "count": 180}
        ]
        with open(targets_file, 'w') as f:
            json.dump(dummy_data, f, indent=2)
        logger.info("Created dummy targets.json for testing.")

def generate_plan():
    base_dir = "/home/ed/seestar_organizer/data"
    targets_file = os.path.join(base_dir, "targets.json")
    plan_file = os.path.join(base_dir, "tonights_plan.json")
    
    ensure_dummy_library(targets_file)
    
    with open(targets_file, 'r') as f:
        master_targets = json.load(f)

    obs = get_haarlem_observer()
    sun = ephem.Sun()
    
    # Calculate tonight's Astronomical Twilight (Sun at -18 degrees)
    obs.horizon = '-18'
    try:
        dusk = obs.next_setting(sun, use_center=True)
        dawn = obs.next_rising(sun, use_center=True)
    except ephem.AlwaysUpError:
        logger.warning("Summer Solstice! It never gets truly dark tonight.")
        return # Cannot observe

    logger.info(f"Dark Window: {dusk.datetime().strftime('%H:%M')} UTC to {dawn.datetime().strftime('%H:%M')} UTC")
    
    # Set observer time to middle of the dark window to test altitude
    mid_night = dusk.datetime() + (dawn.datetime() - dusk.datetime()) / 2
    obs.date = mid_night
    obs.horizon = str(ALTITUDE_LIMIT)

    tonights_plan = {
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "haarlem_dark_window": {"start": str(dusk), "end": str(dawn)},
        "targets": []
    }

    for target in master_targets:
        star = ephem.FixedBody()
        star._ra = ephem.hours(target['ra'])
        star._dec = ephem.degrees(target['dec'])
        star.compute(obs)
        
        # Is it above our 30-degree horizon limit in the middle of the night?
        alt_deg = float(star.alt) * 180.0 / ephem.pi
        if alt_deg >= ALTITUDE_LIMIT:
            tonights_plan["targets"].append({
                "name": target['name'],
                "ra": float(star._ra) * 12.0 / ephem.pi, # Convert rad to decimal hours for Alpaca
                "dec": float(star._dec) * 180.0 / ephem.pi, # Convert rad to decimal degrees
                "exposure_sec": target.get('exposure', 10),
                "frames": target.get('count', 180),
                "transit_alt": round(alt_deg, 2)
            })
            logger.info(f"✅ {target['name']} passes (Alt: {alt_deg:.1f}°)")
        else:
            logger.warning(f"❌ {target['name']} fails horizon veto (Alt: {alt_deg:.1f}°)")

    with open(plan_file, 'w') as f:
        json.dump(tonights_plan, f, indent=2)
    
    logger.info(f"Plan generated! {len(tonights_plan['targets'])} targets locked.")

if __name__ == "__main__":
    generate_plan()
