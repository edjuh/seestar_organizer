import sys
from pathlib import Path
from astropy.time import Time

# Fix path to find 'core'
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.selector import selector

# Forecast for 16:14 Local / 15:14 UTC
test_time = Time("2026-02-24 15:14:00")

print(f"\n--- Westward-First Night Plan (Forecast: 16:14) ---")
plan = selector.get_night_plan(test_time)

print(f"{'Target':<18} | {'Alt':<7} | {'Az':<7} | {'Status'}")
print("-" * 55)

for t in plan[:10]:
    direction = "WEST (Setting)" if 180 < t['az'] < 350 else "EAST/ZENITH"
    print(f"{t['display_name']:<18} | {t['alt']:>5.1f}° | {t['az']:>5.1f}° | {direction}")

if not plan:
    print("No targets visible in the dark window.")
print("-" * 55 + "\n")
