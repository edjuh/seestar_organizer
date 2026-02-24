from astropy.time import Time
from core.selector import selector
import datetime

# Define 16:14 Local Time for Today
today = datetime.date.today()
target_dt = datetime.datetime(today.year, today.month, today.day, 16, 14)
# Adjust for CET (UTC+1)
target_time = Time(target_dt) - 1 * 3600 * 24 # Astropy uses Julian days for offsets or simpler:
target_time = Time("2026-02-24 15:14:00") # UTC equivalent

print(f"\n--- Top 10 Targets for {target_dt.strftime('%H:%M')} Local ---")
all_targets = selector.get_best_target(target_time)

if all_targets:
    for i, t in enumerate(all_targets[:10], 1):
        print(f"{i:2}. {t['display_name']:15} | Alt: {t['current_alt']:.2f}°")
else:
    print("No targets visible at that time.")
print("-" * 45)
