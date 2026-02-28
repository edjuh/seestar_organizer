#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: core/preflight/nightly_planner.py
Version: 1.2.0 (Pee Pastinakel)
Objective: Generates prioritized target lists based on real-time altitude, scientific urgency, and AAVSO cadence requirements.
"""

import os
import json
import toml
import ephem
import logging
import math
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("NightlyPlanner")

def load_config():
    with open(os.path.expanduser("~/seestar_organizer/config.toml"), 'r') as f:
        return toml.load(f)

def is_due(target, now_date):
    """Checks if a target is due for observation based on cadence."""
    last = target.get('last_observed')
    if not last: return True
    
    last_dt = datetime.strptime(last, "%Y-%m-%d")
    cadence = target.get('cadence_days', 1)
    return (now_date - last_dt).days >= cadence

def execute_planning():
    config = load_config()
    loc = config['location']
    
    obs = ephem.Observer()
    obs.lat, obs.lon = str(loc['lat']), str(loc['lon'])
    obs.horizon = str(config.get('planner', {}).get('sun_altitude_limit', -18.0))
    
    dusk = obs.next_setting(ephem.Sun(), use_center=True)
    dawn = obs.next_rising(ephem.Sun(), use_center=True)
    budget_sec = ((dawn - dusk) * 86400) - 3600

    data_dir = os.path.expanduser(config['storage'].get('target_dir', '~/seestar_organizer/data'))
    with open(os.path.join(data_dir, "targets.json"), 'r') as f:
        targets = json.load(f)

    now_date = datetime.now()
    due_targets = [t for t in targets if is_due(t, now_date)]
    
    logger.info(f"📊 Filtering: {len(targets)} total -> {len(due_targets)} due.")

    obs.date = dusk
    final_candidates = []
    for t in due_targets:
        star = ephem.FixedBody()
        star._ra = ephem.hours(t['ra'] / 15.0)
        star._dec = ephem.degrees(t['dec'])
        star.compute(obs)
        
        alt = float(star.alt) * 180.0 / math.pi
        if alt < loc.get('horizon_limit', 30.0): continue

        airmass = 1.0 / math.cos((90 - alt) * math.pi / 180.0)
        score = (2000 if t.get('priority') else 0) + (100 / airmass)
        
        final_candidates.append({**t, "score": score, "airmass": round(airmass, 2)})

    final_candidates.sort(key=lambda x: x['score'], reverse=True)
    plan = []
    remaining = budget_sec
    
    for c in final_candidates:
        if remaining <= 0: break
        slot_sec = 600
        plan.append({
            "name": c['star_name'],
            "ra": c['ra'], "dec": c['dec'],
            "exposure_sec": 60,
            "frames": 4,
            "airmass_start": c['airmass']
        })
        remaining -= slot_sec

    with open(os.path.join(data_dir, "tonights_plan.json"), 'w') as f:
        json.dump(plan, f, indent=4)
    
    logger.info(f"✅ Created plan with {len(plan)} targets.")

if __name__ == "__main__":
    execute_planning()
