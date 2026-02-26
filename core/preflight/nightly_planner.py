#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: core/preflight/nightly_planner.py
Version: 1.1.0 (Kwetal)
Role: Preflight C - The Scheduler
Objective: Scores targets against Haarlem ephemeris and lands plan in the Flight Data deck.
"""

import os
import sys
import json
import toml
import ephem
from datetime import datetime, timezone
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("NightlyPlanner")

def load_observatory_config():
    config_path = "/home/ed/seestar_organizer/config.toml"
    if not os.path.exists(config_path):
        logger.error(f"Config file missing at {config_path}")
        sys.exit(1)
        
    try:
        with open(config_path, 'r') as f:
            config = toml.load(f)
            
        loc = config.get('location', {})
        hw = config.get('hardware', {})
        
        lat = loc.get('lat') 
        lon = loc.get('lon')
        alt_limit = loc.get('horizon_limit', 30.0)
        default_exp = hw.get('default_exposure', 60) # Updated for standard science frames
        moon_limit = loc.get('moon_avoidance', 30.0) 
        
        if lat is None or lon is None:
            logger.error("Latitude/Longitude missing in config.toml.")
            sys.exit(1)
            
        return str(lat), str(lon), float(alt_limit), int(default_exp), float(moon_limit)
        
    except Exception as e:
        logger.error(f"Failed to parse config.toml: {e}")
        sys.exit(1)

def format_filename(star_name):
    return star_name.lower().replace(" ", "_") + ".json"

def generate_plan():
    lat, lon, alt_limit, default_exp, moon_limit = load_observatory_config()
    logger.info(f"Observer: {lat}°N, {lon}°E | Horizon: {alt_limit}° | Moon Avoid: {moon_limit}°")

    # Path Logic: Data (Input) vs Flight Data (Output)
    base_data_dir = "/home/ed/seestar_organizer/data"
    flight_data_dir = "/home/ed/seestar_organizer/core/flight/data"
    
    targets_file = os.path.join(base_data_dir, "targets.json")
    comp_dir = os.path.join(base_data_dir, "comp_stars")
    plan_file = os.path.join(flight_data_dir, "tonights_plan.json")
    
    if not os.path.exists(targets_file):
        logger.error(f"Missing master targets file: {targets_file}")
        sys.exit(1)
        
    if not os.path.exists(flight_data_dir):
        os.makedirs(flight_data_dir, exist_ok=True)
    
    with open(targets_file, 'r') as f:
        master_targets = json.load(f)

    obs = ephem.Observer()
    obs.lat, obs.lon, obs.elevation = lat, lon, 0
    obs.date = datetime.now(timezone.utc)
    sun, moon = ephem.Sun(), ephem.Moon()
    
    obs.horizon = '-18'
    try:
        dusk = obs.next_setting(sun, use_center=True)
        dawn = obs.next_rising(sun, use_center=True)
    except ephem.AlwaysUpError:
        logger.warning("Summer Solstice condition detected.")
        return 

    logger.info(f"Dark Window: {dusk.datetime().strftime('%H:%M')} UTC to {dawn.datetime().strftime('%H:%M')} UTC")
    mid_night = dusk.datetime() + (dawn.datetime() - dusk.datetime()) / 2
    obs.horizon = str(alt_limit)

    scored_targets = []
    seen_targets = set()

    for target in master_targets:
        t_name = target.get('star_name')
        t_ra_deg, t_dec_deg = target.get('ra'), target.get('dec')
        
        if not t_name or t_ra_deg is None or t_dec_deg is None or t_name in seen_targets:
            continue

        # Comparison Star Check (Integrity Check)
        expected_comp_file = os.path.join(comp_dir, format_filename(t_name))
        if not os.path.exists(expected_comp_file):
            continue

        star = ephem.FixedBody()
        star._ra = float(t_ra_deg) * ephem.pi / 180.0
        star._dec = float(t_dec_deg) * ephem.pi / 180.0
        
        obs.date = mid_night
        star.compute(obs)
        moon.compute(obs)
        separation = ephem.separation(star, moon) * 180.0 / ephem.pi
        
        if separation < moon_limit:
            continue
            
        alt_mid = float(star.alt) * 180.0 / ephem.pi
        if alt_mid < alt_limit:
            continue

        score = 1000 if target.get('priority') is True else 0
        
        obs.date = dusk
        star.compute(obs)
        alt_dusk = float(star.alt) * 180.0 / ephem.pi
        
        obs.date = dawn
        star.compute(obs)
        alt_dawn = float(star.alt) * 180.0 / ephem.pi
        
        if alt_dusk > alt_dawn: score += 500
        score += alt_mid
        
        scored_targets.append({
            "name": t_name,
            "ra": round(float(t_ra_deg) / 15.0, 6), 
            "dec": round(float(t_dec_deg), 6),
            "exposure_sec": default_exp,
            "frames": 180, 
            "transit_alt": round(alt_mid, 2),
            "filter": target.get('filter', 'V'),
            "score": round(score, 1)
        })
        seen_targets.add(t_name)

    scored_targets.sort(key=lambda x: x['score'], reverse=True)
    top_targets = scored_targets[:20]

    tonights_plan = {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "local_dark_window": {"start": str(dusk), "end": str(dawn)},
        "targets": top_targets
    }

    with open(plan_file, 'w') as f:
        json.dump(tonights_plan, f, indent=2)
    
    logger.info(f"Aeronautical Plan generated: {plan_file}")

if __name__ == "__main__":
    generate_plan()
