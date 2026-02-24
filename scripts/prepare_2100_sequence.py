"""
Filename: scripts/prepare_2100_sequence.py
Objective: Forecast and prepare a science-grade sequence for 21:00 tonight.
"""
from core.selector import Selector
from datetime import datetime, time

# Target time: 21:00:00 tonight
target_hour = datetime.combine(datetime.now().date(), time(21, 0))

# Initialize Williamina's selector
williamina = Selector(specialist="WILLIAMINA")
plan = williamina.get_night_plan(target_time=target_hour)

if plan:
    top_target = plan[0]
    print(f"\n--- 21:00 Observation Plan (Williamina) ---")
    print(f"Target: {top_target['display_name']}")
    print(f"Coordinates: RA {top_target['ra']}, DEC {top_target['dec']}")
    print(f"Forecast Alt: {top_target['alt']:.2f}° | Az: {top_target['az']:.2f}°")
    print(f"Priority Score: {top_target['priority_score']:.2f}")
    
    # Payload Construction for Alpaca
    payload = {
        "target_name": top_target['display_name'],
        "ra": top_target['ra'],
        "dec": top_target['dec'],
        "is_j2000": True,
        "panel_time_sec": 60 # Standard variable star exposure
    }
    print(f"\nPayload Ready for Federation Injection at /1/schedule")
else:
    print("No targets meet the science criteria for 21:00.")
