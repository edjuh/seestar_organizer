#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: core/selector.py
Version: 1.2.0 (Pee Pastinakel)
Objective: Prioritize targets setting in the West during the dark window.
"""

import os
import json
from core.ephemeris import observer
from core.logger import log_event
from core.hardware_profiles import get_profile

class Selector:
    def __init__(self, specialist="WILLIAMINA"):
        """Initialize with a specific hardware specialist profile."""
        self.vault_path = "data/sequences/"
        self.profile = get_profile(specialist)
        log_event(f"Selector: Active Specialist is {specialist} ({self.profile['model']})")

    def get_night_plan(self, target_time=None):
        """Finds valid targets and ranks them by western urgency and hardware FOV."""
        targets_found = []

        if not os.path.exists(self.vault_path):
            log_event(f"Selector: Vault path missing!", level="error")
            return []

        files = [f for f in os.listdir(self.vault_path) if f.endswith('.json')]
        
        for filename in files:
            try:
                with open(os.path.join(self.vault_path, filename), 'r') as f:
                    raw_data = json.load(f)
                
                # Handle AAVSO list-wrapped JSON
                data = raw_data if isinstance(raw_data, list) else raw_data
                ra, dec = data.get('ra'), data.get('dec')
                if ra is None or dec is None: continue
                
                pos = observer.get_alt_az(ra, dec, time_override=target_time)
                
                # Filter: Altitude Gate
                if pos['alt'] > 30:
                    data['display_name'] = data.get('auid') or data.get('comments') or filename
                    data['alt'] = pos['alt']
                    data['az'] = pos['az']
                    
                    # Westward Priority Logic
                    if 180 < pos['az'] < 350:
                        data['priority_score'] = 100 - pos['alt'] 
                    else:
                        data['priority_score'] = pos['alt'] / 2

                    targets_found.append(data)
            except Exception:
                continue

        targets_found.sort(key=lambda x: x['priority_score'], reverse=True)
        return targets_found

if __name__ == "__main__":
    selector = Selector()
    plan = selector.get_night_plan()
    print(f"✅ Selector: Found {len(plan)} valid targets.")
