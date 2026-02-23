from core.vault_manager import vault_manager
from astropy.time import Time, TimeDelta
from astropy.coordinates import SkyCoord, AltAz
import astropy.units as u

targets = [
    {"name": "MU Cam", "ra": "03:53:18", "dec": "+62:11:48"},
    {"name": "SS Cyg", "ra": "21:42:45", "dec": "+43:35:08"},
    {"name": "Algol",  "ra": "03:08:10", "dec": "+40:57:20"},
    {"name": "RR Lyr", "ra": "19:22:33", "dec": "+42:47:03"}
]

def analyze_night():
    now = Time.now()
    # Looking ahead 12 hours in 30-min increments
    time_steps = [now + TimeDelta(i*1800, format='sec') for i in range(24)]
    
    print(f"📅 Haarlem Night Forecast: {now.strftime('%Y-%m-%d')}")
    print(f"{'TARGET':<12} | {'MAX ALT':<10} | {'WINDOW START':<15} | {'WINDOW END':<15}")
    print("-" * 65)

    for t in targets:
        coord = SkyCoord(t['ra'], t['dec'], unit=(u.hourangle, u.deg))
        altitudes = []
        window_times = []

        for check_time in time_steps:
            altaz = coord.transform_to(AltAz(obstime=check_time, location=vault_manager.location))
            alt = altaz.alt.degree
            altitudes.append(alt)
            if alt >= 30:
                window_times.append(check_time)

        if window_times:
            max_alt = max(altitudes)
            start = window_times[0].datetime.strftime('%H:%M')
            end = window_times[-1].datetime.strftime('%H:%M')
            print(f"{t['name']:<12} | {max_alt:>7.1f}° | {start:<15} | {end:<15}")
        else:
            print(f"{t['name']:<12} | NEVER CROSSES 30° TONIGHT")

if __name__ == "__main__":
    analyze_night()
