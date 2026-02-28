#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Objective: Score 1,240 targets against tonights sky and pick the Top 20.
"""
"""
Filename: core/planning/nightly_planner.py
Version: 1.0.0 (Kwetal)
Role: Preflight C - The Scheduler
"""

import json
import tomllib
from datetime import datetime
from pathlib import Path
from astropy.coordinates import EarthLocation, AltAz, SkyCoord, get_moon
from astropy.time import Time
import astropy.units as u

# --- SETUP ---
project_root = Path(__file__).parent.parent.parent
config_path = project_root / "config.toml"
targets_path = project_root / "data/targets.json"

def get_plan():
    with open(config_path, "rb") as f:
        cfg = tomllib.load(f)
    
    loc = EarthLocation(
        lat=cfg['location']['latitude']*u.deg, 
        lon=cfg['location']['longitude']*u.deg, 
        height=cfg['location']['elevation']*u.m
    )
    now = Time.now()
    min_alt = cfg['location']['min_altitude']
    
    with open(targets_path, 'r') as f:
        targets = json.load(f)

    # 1. Calculate Sky State
    altaz_frame = AltAz(obstime=now, location=loc)
    moon = get_moon(now).transform_to(altaz_frame)
    
    scored_targets = []
    for t in targets:
        coord = SkyCoord(ra=t['ra']*u.deg, dec=t['dec']*u.deg, frame='icrs')
        pos = coord.transform_to(altaz_frame)
        
        # 2. Veto: Horizon & Lunar Proximity
        if pos.alt.degree < min_alt: continue
        moon_dist = pos.separation(moon).degree
        if moon_dist < 15: continue # Too close to the moon

        # 3. Scoring: Priority + Altitude + Setting (West)
        score = 100 if t.get('priority') else 0
        score += pos.alt.degree  # High altitude is better
        if 180 < pos.az.degree < 270: score += 50 # Reward Setting West

        scored_targets.append({
            "name": t['star_name'],
            "alt": round(pos.alt.degree, 1),
            "az": round(pos.az.degree, 1),
            "score": round(score, 1)
        })

    # 4. Sort and Cap to Top 20
    scored_targets.sort(key=lambda x: x['score'], reverse=True)
    plan = scored_targets[:20]

    with open(project_root / "data/tonights_plan.json", "w") as f:
        json.dump(plan, f, indent=4)
    
    print(f"✅ Generated Plan: {len(plan)} targets selected for the Top 20.")

if __name__ == "__main__":
    get_plan()
