"""
Filename: core/stellarmate_api.py
Version: 0.7.3
Role: Interface for StellarMate REST API and Scheduler Image retrieval.
Owner: Ed de la Rie (PE5ED)
"""
import requests
from pathlib import Path

class StellarMateAPI:
    def __init__(self, config: dict):
        conn = config.get("connections", {})
        host = conn.get("stellarmate_host", "stellarmate.local")
        port = conn.get("stellarmate_port", 5432)
        self.base_url = f"http://{host}:{port}/0"
        self.timeout = 5

    def get_scheduler_status(self) -> dict:
        """Fetches the current scheduler state (active job, progress, etc.)"""
        try:
            r = requests.get(f"{self.base_url}/schedule", timeout=self.timeout)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            return {"error": str(e)}

    def download_scheduler_image(self, dest_path: str = "logs/scheduler_live.jpg") -> bool:
        """
        Sidesteps to the endpoint you noted.
        Downloads the current scheduler/guider/image preview.
        """
        url = f"{self.base_url}/schedule/image"
        try:
            r = requests.get(url, stream=True, timeout=self.timeout)
            r.raise_for_status()
            with open(dest_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        except Exception:
            return False

    def get_telescope_info(self) -> dict:
        """Direct access to telescope coords via StellarMate API."""
        try:
            r = requests.get(f"{self.base_url}/telescope", timeout=self.timeout)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            return {"error": str(e)}
