#!/usr/bin/env python3
import requests
import json
import logging

logger = logging.getLogger("AlpacaClient")

class AlpacaClient:
    def __init__(self, host="127.0.0.1", port=5555):
        self.base_url = f"http://{host}:{port}/api/v1/telescope/1"

    def is_connected(self):
        try:
            r = requests.get(f"{self.base_url}/connected", timeout=2)
            return r.json().get("Value", False)
        except: return False

    def start_1x1_mosaic(self, target_name, ra, dec):
        """Sends the Mosaic command as an Alpaca 'Action' to Device 1."""
        payload = {
            "Action": "start_mosaic",
            "Parameters": json.dumps({
                "target_name": target_name,
                "ra": ra,
                "dec": dec,
                "ra_num": 1,
                "dec_num": 1
            }),
            "ClientID": 1,
            "ClientTransactionID": int(time.time())
        }
        try:
            # Note: Using PUT to the 'action' endpoint as per Alpaca spec
            r = requests.put(f"{self.base_url}/action", data=payload, timeout=5)
            return r.json().get("ErrorNumber", 0) == 0
        except Exception as e:
            logger.error(f"Injection Failed: {e}")
            return False
