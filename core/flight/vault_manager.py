"""
Filename: core/vault_manager.py
Version: 0.9.6 (TOML Integrated)
Role: Configuration-driven Librarian
Objective: Maps to the user's existing config.toml structure.
"""
import toml
from pathlib import Path
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time
import astropy.units as u

class VaultManager:
    def __init__(self):
        config_path = Path("config.toml")
        if config_path.exists():
            conf = toml.load(config_path)
            # Mapping to your specific [location] keys
            loc = conf.get('location', {})
            self.lat = loc.get('lat', 52.38)
            self.lon = loc.get('lon', 4.64)
            self.elev = loc.get('elevation', 2.0)
            self.min_altitude = loc.get('horizon_limit', 30.0)
        else:
            self.lat, self.lon, self.elev, self.min_altitude = 52.38, 4.64, 2, 30.0

        self.location = EarthLocation(lat=self.lat*u.deg, lon=self.lon*u.deg, height=self.elev*u.m)

    def get_target_visibility(self, ra_str, dec_str):
        now = Time.now()
        target = SkyCoord(ra_str, dec_str, unit=(u.hourangle, u.deg))
        altaz_frame = AltAz(obstime=now, location=self.location)
        target_altaz = target.transform_to(altaz_frame)
        
        current_alt = target_altaz.alt.degree
        is_observable = current_alt >= self.min_altitude
        
        return round(current_alt, 2), is_observable

vault_manager = VaultManager()
