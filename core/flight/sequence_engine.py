"""
Filename: core/flight/sequence_engine.py
Version: 1.2.1 (Resilient Logic)
Role: The Night's Conductor
Objective: Prioritizes targets without crashing on vault attributes.
"""
import logging

logger = logging.getLogger("SequenceEngine")

class SequenceEngine:
    def __init__(self):
        # Setting defaults to avoid AttributeError during simulation
        self.horizon = 30.0
        self.FORCE_SIMULATION = True 

    def build_night_plan(self, target_list):
        """
        In FORCE_SIMULATION mode, visibility checks are bypassed.
        """
        plan = []
        for t in target_list:
            if self.FORCE_SIMULATION:
                alt = t.get('transit_alt', 45.0) 
                observable = True
                logger.info(f"SIMULATION: Force-loading {t['name']}")
            else:
                # Placeholder for real visibility logic
                alt, observable = 45.0, True
            
            if observable:
                plan.append({
                    "name": t['name'],
                    "ra": t['ra'],
                    "dec": t['dec'],
                    "current_alt": alt,
                    "priority": "HIGH" if alt < 45 else "NORMAL"
                })
        
        plan.sort(key=lambda x: x['current_alt'])
        return plan

sequence_engine = SequenceEngine()
