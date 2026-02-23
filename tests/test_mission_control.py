from core.sequence_engine import sequence_engine

# Simulated Target Database
golden_four = [
    {"name": "MU Cam", "ra": "03:53:18", "dec": "+62:11:48"},
    {"name": "SS Cyg", "ra": "21:42:45", "dec": "+43:35:08"},
    {"name": "Algol",  "ra": "03:08:10", "dec": "+40:57:20"},
    {"name": "RR Lyr", "ra": "19:22:33", "dec": "+42:47:03"}
]

print("🚀 SEESTAR MISSION CONTROL: NIGHTLY BRIEFING")
print("-" * 50)

mission_plan = sequence_engine.build_night_plan(golden_four)

for i, task in enumerate(mission_plan, 1):
    print(f"{i}. [PRIORITY: {task['priority']}] Target: {task['name']}")
    print(f"   Coords: {task['ra']}, {task['dec']}")
    print(f"   Current Alt: {task['current_alt']}° (Tracking...)\n")

print("✨ All sequences ready for Alpaca injection.")
