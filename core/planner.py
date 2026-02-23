"""
Filename: core/planner.py
Version: 1.1.0
Role: Solar Ephemeris & Night Planning
Objective: Calculates darkness windows for Haarlem for any given date.
"""
from astropy.coordinates import get_sun, AltAz
from astropy.time import Time
from core.vault_manager import vault_manager
import astropy.units as u

class NightPlanner:
    def __init__(self):
        self.location = vault_manager.location

    def get_darkness_window(self, date_str=None):
        """
        Calculates when the sun drops below -12 (Nautical) or -18 (Astro).
        Default is 'now'. Format for date_str: '2026-03-02 12:00:00'
        """
        check_time = Time.now() if not date_str else Time(date_str)
        
        # We check a 24-hour range to find the dip
        times = check_time + (range(0, 24) * u.hour)
        sun_coords = get_sun(times)
        altaz_frame = AltAz(obstime=times, location=self.location)
        sun_altaz = sun_coords.transform_to(altaz_frame)
        
        # Filter for times where sun < -12 (Nautical Twilight)
        dark_times = times[sun_altaz.alt < -12*u.deg]
        
        if len(dark_times) > 0:
            return dark_times[0], dark_times[-1]
        return None, None

planner = NightPlanner()
