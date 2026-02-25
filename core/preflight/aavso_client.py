"""
Filename: core/aavso_client.py
Objective: AAVSO VSP API interface with intelligent error parsing and FOV scaling.
"""
import requests
from requests.auth import HTTPBasicAuth
from core.env_loader import cfg
from core.logger import log_event

class AAVSOClient:
    def __init__(self):
        self.base_url = "https://app.aavso.org/vsp/api/chart/"
        self.api_key = cfg("AAVSO_TARGET_KEY")
        self.auth = HTTPBasicAuth(self.api_key, 'api_token') if self.api_key else None
        self.headers = {'User-Agent': 'S30-PRO-Seestar/1.0', 'Accept': 'application/json'}

    def fetch_sequence(self, star_name):
        # Clean double spaces to prevent 400 Bad Request
        clean_star = " ".join(star_name.split())
        
        # FOV 240 arcminutes (4 deg) leverages the S30 Pro Telephoto FOV
        params = {"star": clean_star, "format": "json", "fov": 240, "maglimit": 18.0}
        
        try:
            response = requests.get(self.base_url, params=params, headers=self.headers, auth=self.auth, timeout=20)
            
            # Try to read the JSON first, regardless of HTTP status
            try:
                data = response.json()
            except ValueError:
                data = {}

            if not response.ok:
                error_msg = data.get("errors", [response.reason])[0]
                log_event(f"AAVSO Rejected '{clean_star}': {error_msg}", level="warning")
                return None
                
            photometry = data.get("photometry", [])
            if not photometry:
                log_event(f"AAVSO returned empty sequence for '{clean_star}'.", level="warning")
                return None
                
            return photometry
            
        except requests.exceptions.Timeout:
            log_event(f"AAVSO Connection Timeout for {star_name}", level="error")
            return None
        except Exception as e:
            log_event(f"AAVSO Network Error for {star_name}: {e}", level="error")
            return None

client = AAVSOClient()
