import sys
from pathlib import Path

# Add project root to sys.path so we can find 'core'
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.ephemeris import observer

targets = [
    {"name": "SS Cygni", "ra": "21h42m42s", "dec": "+43d35m10s"},
    {"name": "RR Lyrae", "ra": "19h25m28s", "dec": "+42d47m04s"}
]

print(f"\n--- Kwetal Sight Check (Haarlem Local Time) ---")
for t in targets:
    pos = observer.get_alt_az(t['ra'], t['dec'])
    status = "VISIBLE ✅" if pos['is_visible'] else "TOO LOW ❌"
    print(f"{t['name']}: Alt {pos['alt']:.2f}°, Az {pos['az']:.2f}° -> {status}")
print("-" * 45 + "\n")
