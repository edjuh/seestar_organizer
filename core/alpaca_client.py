"""
Filename: core/alpaca_client.py
Objective: Handshake with the Seestar Federation Alpaca bridge (Port 5432).
"""
import requests
import os
import uuid
from core.logger import log_event

class AlpacaClient:
    def __init__(self):
        host = os.getenv("ALPACA_HOST", "127.0.0.1")
        port = os.getenv("ALPACA_PORT", "5432")
        self.base_url = f"http://{host}:{port}"
        self.timeout = (3.1, 30.0)

    def park_telescope(self):
        url = f"{self.base_url}/0/schedule"
        payload = {
            "list": [
                {"action": "scope_park", "params": {}, "schedule_item_id": str(uuid.uuid4())},
                {"action": "shutdown", "params": {}, "schedule_item_id": str(uuid.uuid4())}
            ]
        }
        return self._send_to_scheduler(url, payload, "Emergency Park")

    def start_observation(self, target):
        url = f"{self.base_url}/0/schedule"
        # Use display_name as defined in Selector
        name = target.get('display_name') or target.get('auid') or "Unknown"
        
        payload = {
            "list": [{
                "action": "start_mosaic",
                "params": {
                    "target_name": name,
                    "ra": target['ra'],
                    "dec": target['dec'],
                    "is_j2000": True,
                    "panel_time_sec": 60,
                    "gain": 80
                },
                "schedule_item_id": str(uuid.uuid4())
            }]
        }
        return self._send_to_scheduler(url, payload, f"Observation: {name}")

    def _send_to_scheduler(self, url, payload, desc):
        try:
            r = requests.post(url, json=payload, timeout=self.timeout)
            r.raise_for_status()
            log_event(f"Alpaca: {desc} ACCEPTED.")
            return True
        except Exception as e:
            log_event(f"Alpaca: {desc} FAILED: {e}", level="error")
            return False

alpaca = AlpacaClient()
