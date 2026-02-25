"""
Filename: core/sequence_engine.py
Version: 1.1.0
Role: The Night's Conductor
Objective: Prioritizes targets and creates a time-slotted mission plan.
"""
from core.vault_manager import vault_manager
from astropy.time import Time, TimeDelta
from astropy.coordinates import SkyCoord, AltAz
import astropy.units as u

class SequenceEngine:
    def __init__(self):
        self.location = vault_manager.location
        self.horizon = vault_manager.min_altitude

    def build_night_plan(self, target_list):
        """
        Takes a list of targets and sorts them by 'Imaging Priority' 
        (closest to setting soonest gets higher priority).
        """
        plan = []
        now = Time.now()
        
        for t in target_list:
            alt, observable = vault_manager.get_target_visibility(t['ra'], t['dec'])
            
            # Simplified Logic: If it's visible, we want to know when it sets
            if observable:
                # Find setting time (when it hits horizon_limit)
                # For this MVP, we label them by current altitude
                plan.append({
                    "name": t['name'],
                    "ra": t['ra'],
                    "dec": t['dec'],
                    "current_alt": alt,
                    "priority": "HIGH" if alt < 45 else "NORMAL"
                })
        
        # Sort by altitude ascending (Catch the sinking targets first!)
        plan.sort(key=lambda x: x['current_alt'])
        return plan

sequence_engine = SequenceEngine()
