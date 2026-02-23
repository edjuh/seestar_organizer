"""
Filename: core/alpaca_client.py
Objective: ASCOM Alpaca interface for Seestar S50 hardware control.
Usage: Internal module used by Orchestrator.
Note: Communicates with the Seestar via REST API on port 4567.
"""
import requests
from core.env_loader import cfg
from core.logger import log_event

class AlpacaClient:
    def __init__(self):
        self.ip = cfg("SEESTAR_IP", "192.168.1.1")
        self.port = 4567
        self.base_url = f"http://{self.ip}:{self.port}/api/v1"
        self.transaction_id = 0

    def _get_tid(self):
        self.transaction_id += 1
        return self.transaction_id

    def put(self, device_type, device_id, method, **params):
        url = f"{self.base_url}/{device_type}/{device_id}/{method}"
        params['ClientTransactionID'] = self._get_tid()
        try:
            response = requests.put(url, data=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            log_event(f"Alpaca PUT Error ({method}): {e}", level="error")
            return {"Success": False, "Message": str(e)}

    def get(self, device_type, device_id, method):
        url = f"{self.base_url}/{device_type}/{device_id}/{method}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            log_event(f"Alpaca GET Error ({method}): {e}", level="error")
            return None

alpaca = AlpacaClient()
