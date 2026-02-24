import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.selector import selector

print("\n--- Kwetal Vault Audit ---")
best = selector.get_best_target()

if best:
    print(f"WINNER  : {best['display_name']}")
    print(f"ALTITUDE: {best['current_alt']:.2f}°")
    print(f"RA/DEC  : {best['ra']} / {best['dec']}")
else:
    print("No valid targets found above 30° altitude.")
print("-" * 25 + "\n")
