import requests
import sys
from pathlib import Path

# Ensure paths
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from core.env_loader import cfg
from utils.astro import ra_to_decimal, dec_to_decimal

class AlpacaClient:
    def __init__(self):
        # Grabs the http://0.0.0.0:5555 from config.toml
        self.base_url = cfg("hardware", "seestar_bridge_url", "http://0.0.0.0:5555")
        self.sequence_url = f"{self.base_url}/api/v1/telescope/0/sequence"

    def inject_mission(self, target_name, ra, dec, exp_time=10, count=30):
        """
        The 'Golden Bridge' payload. 
        Forces seestar_alp to Plate-Solve and center using a 1x1 Mosaic.
        """
        # Ensure coordinates are decimal
        ra_deg = ra_to_decimal(ra)
        dec_deg = dec_to_decimal(dec)
        
        payload = {
            "targets": [{
                "name": target_name,
                "ra": ra_deg,
                "dec": dec_deg,
                "exposure_time": exp_time,
                "count": count,
                "type": "mosaic",
                "mosaic_settings": {
                    "rows": 1,
                    "cols": 1,
                    "overlap": 0
                }
            }]
        }
        
        print(f"🚀 Injecting Mission: {target_name} ({count}x{exp_time}s)")
        print(f"📡 Payload sent to {self.sequence_url}...")
        
        try:
            r = requests.post(self.sequence_url, json=payload, timeout=10)
            
            # Since the mock or real bridge might return different things,
            # we check for a 200 OK or 202 Accepted.
            if r.status_code in (200, 201, 202):
                print("✅ Mission successfully injected into Sequencer.")
                return True
            else:
                print(f"❌ Sequencer rejected payload. HTTP {r.status_code}")
                print(r.text)
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection to Alpaca Bridge failed: {e}")
            return False

# Quick test block if executed directly
if __name__ == "__main__":
    client = AlpacaClient()
    # Sending SS Cyg with raw Decimal Degrees
    client.inject_mission("SS Cyg", 325.68, 43.58, 10, 30)
