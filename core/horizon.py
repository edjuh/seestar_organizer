"""
Filename: core/horizon.py
Objective: Veto targets based on local obstructions (Trees, Buildings).
"""

# Simple Azimuth: Min_Alt map
# Example: Between 150° and 210° (South), I need at least 45° altitude to clear the roof.
OBSTRUCTIONS = [
    {"az_start": 150, "az_end": 210, "min_alt": 45},
    {"az_start": 300, "az_end": 350, "min_alt": 55}, # A big tree in the NW
]

def is_obstructed(az, alt):
    for obs in OBSTRUCTIONS:
        if obs["az_start"] <= az <= obs["az_end"]:
            if alt < obs["min_alt"]:
                return True
    return False
