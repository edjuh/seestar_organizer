"""
Filename: core/selector.py
Objective: Prioritize targets setting in the West during the dark window.
"""
import os
import json
from core.ephemeris import observer
from core.logger import log_event

class Selector:
    def __init__(self):
        self.vault_path = "data/sequences/"

    def get_night_plan(self, target_time=None):
        """Finds all valid targets and ranks them by western urgency."""
        targets_found = []

        if not os.path.exists(self.vault_path):
            log_event(f"Selector: Vault path missing!", level="error")
            return []

        files = [f for f in os.listdir(self.vault_path) if f.endswith('.json')]
        
        for filename in files:
            try:
                with open(os.path.join(self.vault_path, filename), 'r') as f:
                    raw_data = json.load(f)
                
                data = raw_data[0] if isinstance(raw_data, list) else raw_data
                ra, dec = data.get('ra'), data.get('dec')
                if ra is None or dec is None: continue
                
                pos = observer.get_alt_az(ra, dec, time_override=target_time)
                
                # Filter: Must be above the 30-degree floor
                if pos['alt'] > 30:
                    data['display_name'] = data.get('auid') or data.get('comments') or filename
                    data['alt'] = pos['alt']
                    data['az'] = pos['az']
                    
                    # Logic: If Azimuth is West (180-350) and Alt is low, it's high priority
                    # We create a 'priority_score'. Higher = Capture it now.
                    if 180 < pos['az'] < 350:
                        # Urgency increases as altitude decreases toward 30
                        data['priority_score'] = 100 - pos['alt'] 
                    else:
                        # Eastern/Zenith objects have lower priority than setting objects
                        data['priority_score'] = pos['alt'] / 2

                    targets_found.append(data)
            except Exception:
                continue

        # Sort by priority score (Urgent/Western first)
        targets_found.sort(key=lambda x: x['priority_score'], reverse=True)
        return targets_found

selector = Selector()
