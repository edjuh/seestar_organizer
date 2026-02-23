"""
Filename: core/aavso_client.py
Objective: AAVSO VSP API interface with verified app.aavso.org URL and Basic Auth.
"""
import requests
from requests.auth import HTTPBasicAuth
from core.env_loader import cfg
from core.logger import log_event

class AAVSOClient:
    def __init__(self):
        # Canonical URL for API access
        self.base_url = "https://app.aavso.org/vsp/api/chart/"
        self.api_key = cfg("AAVSO_TARGET_KEY")
        self.auth = HTTPBasicAuth(self.api_key, 'api_token') if self.api_key else None
        self.headers = {
            'User-Agent': 'S30-PRO-Seestar/1.0',
            'Accept': 'application/json'
        }

    def fetch_sequence(self, star_name):
        params = {"star": star_name, "format": "json", "fov": 60, "maglimit": 18.0}
        try:
            response = requests.get(self.base_url, params=params, headers=self.headers, auth=self.auth, timeout=20)
            response.raise_for_status()
            data = response.json()
            return data.get("photometry", [])
        except Exception as e:
            log_event(f"AAVSO API Error for {star_name}: {e}", level="error")
            return None

client = AAVSOClient()
