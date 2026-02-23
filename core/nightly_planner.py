"""
Filename: core/nightly_planner.py
Version: 1.0.0
Objective: Filter the AAVSO target library for visibility from Haarlem tonight.
Usage: python3 -m core.nightly_planner
Note: Filters for targets > 30 degrees altitude during astronomical night.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from astropy.coordinates import SkyCoord, AltAz, EarthLocation
from astropy.time import Time
import astropy.units as u
from core.gps import gps_location
from core.logger import log_event

class NightlyPlanner:
    def __init__(self):
        self.location = gps_location.get_earth_location()
        self.project_root = Path(__file__).parent.parent
        self.min_altitude = 30 # Degrees

    def generate_manifest(self):
        targets_path = self.project_root / "data" / "targets.json"
        if not targets_path.exists():
            log_event("Planner failed: targets.json missing", level="error")
            return []

        with open(targets_path, 'r') as f:
            all_targets = json.load(f)

        now = Time.now()
        # Create a frame for 'now' at our location
        altaz_frame = AltAz(obstime=now, location=self.location)
        
        tonights_plan = []

        print(f"🔭 Alexander Pieps is calculating for {len(all_targets)} targets...")

        for t in all_targets:
            try:
                # Convert RA/Dec to SkyCoord
                coord = SkyCoord(ra=t['ra']*u.deg, dec=t['dec']*u.deg, frame='icrs')
                altaz = coord.transform_to(altaz_frame)

                # Check if it's currently above our minimum threshold
                if altaz.alt.degree > self.min_altitude:
                    tonights_plan.append({
                        "star_name": t['star_name'],
                        "ra": t['ra'],
                        "dec": t['dec'],
                        "altitude": round(altaz.alt.degree, 1),
                        "azimuth": round(altaz.az.degree, 1),
                        "magnitude": t.get('magnitude', 'N/A')
                    })
            except Exception as e:
                continue

        # Sort by altitude (highest first)
        tonights_plan.sort(key=lambda x: x['altitude'], reverse=True)

        # Save the plan
        plan_path = self.project_root / "data" / "tonights_plan.json"
        with open(plan_path, 'w') as f:
            json.dump(tonights_plan, f, indent=4)

        log_event(f"Generated plan with {len(tonights_plan)} observable targets.")
        return tonights_plan

if __name__ == "__main__":
    planner = NightlyPlanner()
    plan = planner.generate_manifest()
    print(f"✅ Created plan with {len(plan)} targets for Haarlem.")
