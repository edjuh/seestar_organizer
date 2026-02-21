"""
Filename: core/alpaca_sequencer.py
Version: 1.2.0
Purpose: Alpaca client with HMS/DMS to Decimal degree conversion.
"""
import time
import requests
from astropy.coordinates import SkyCoord
import astropy.units as u

class SeestarClient:
    def __init__(self, config: dict):
        self.host = config.get("host", "127.0.0.1")
        self.port = config.get("port", 5555)
        self.base_url = f"http://{self.host}:{self.port}/api/v1"
        self.simulate = config.get("simulate", True)

    def connect(self):
        if self.simulate:
            print("[SIM] SeestarClient initialized in SIMULATION mode.")
            return True
        # Real Alpaca connection logic would go here
        return True

    def slew_and_wait(self, ra, dec):
        """Slews to target, accepting either floats or 'HH:MM:SS' strings."""
        try:
            # COORDINATE GUARD: Convert HMS/DMS strings to Decimal if needed
            if isinstance(ra, str) and ":" in ra:
                c = SkyCoord(ra, dec, unit=(u.hourangle, u.deg))
                ra_deg = c.ra.degree
                dec_deg = c.dec.degree
            else:
                ra_deg = float(ra)
                dec_deg = float(dec)

            if self.simulate:
                print(f"[SIM] Slewing to RA {ra_deg:.4f}, DEC {dec_deg:.4f}")
                time.sleep(2)
                return True
            
            # Placeholder for real Alpaca PUT request
            # requests.put(f"{self.base_url}/telescope/0/slewtocoordinates", 
            #              data={'TargetRightAscension': ra_deg, 'TargetDeclination': dec_deg})
            return True
        except Exception as e:
            print(f"[SEQ ERROR] Slew failed: {e}")
            return False

    def expose_and_wait(self, seconds):
        if self.simulate:
            print(f"[SIM] Starting {seconds}s exposure...")
            time.sleep(seconds)
            print("[SEQ] Exposure Finished.")
            return True
        # Real camera trigger logic here
        return True
