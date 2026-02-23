from core.planner import planner
from astropy.time import Time

test_date = "2026-03-02 12:00:00"
start, end = planner.get_darkness_window(test_date)

print(f"🔭 Planning for: {test_date}")
if start:
    print(f"🌑 Nautical Twilight Starts: {start.datetime.strftime('%H:%M')} UTC")
    print(f"🌅 Nautical Twilight Ends:   {end.datetime.strftime('%H:%M')} UTC")
    print(f"⏱️ Total Imaging Window:    {round((end - start).value * 24, 2)} hours")
else:
    print("⚠️ No darkness window found (Midnight Sun scenario?)")
