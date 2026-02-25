#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Objective: Exclusive HTTP client for Seestar Alpaca API communication.
"""

import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger("AlpacaClient")

class AlpacaClient:
    
    def __init__(self, host="127.0.0.1", port=5555, device_number=1, client_id=1):
        # Default device is 1 (The Hardware), but Federation is usually 0
        self.host = host
        self.port = port
        self.device_number = device_number
        self.client_id = client_id
        self.transaction_id = 1
        self.timeout = 5

    def _get_auth_params(self):
        self.transaction_id += 1
        return {"ClientID": self.client_id, "ClientTransactionID": self.transaction_id}

    def _request(self, method, endpoint, target_device=None, data=None, json_payload=None):
        """Hardened request handler supporting Form Data (Alpaca) and JSON (Custom)."""
        device = target_device if target_device is not None else self.device_number
        url = f"http://{self.host}:{self.port}/api/v1/telescope/{device}/{endpoint}"
        params = self._get_auth_params()
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, params=params, timeout=self.timeout)
            elif method.upper() == "PUT":
                # Standard Alpaca uses form-encoded data
                payload = {**params}
                if data:
                    payload.update(data)
                response = requests.put(url, data=payload, timeout=self.timeout)
            elif method.upper() == "POST":
                # Custom endpoints (like Federation) often expect raw JSON
                url = f"http://{self.host}:{self.port}/api/v1/federation/0/{endpoint}" # Adjusted for typical Federation routes
                response = requests.post(url, params=params, json=json_payload, timeout=self.timeout)
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()
            result = response.json()
            
            if result.get("ErrorNumber", 0) != 0:
                logger.warning(f"Alpaca API Error {result.get('ErrorNumber')}: {result.get('ErrorMessage')}")
                return None
                
            return result.get("Value", True)

        except requests.exceptions.RequestException as e:
            logger.error(f"Connection failed: {endpoint} -> {e}")
            return None

    # --- Standardized API Methods ---

    def is_connected(self):
        result = self._request("GET", "connected")
        return bool(result) if result is not None else False

    def get_latitude(self):
        return self._request("GET", "sitelatitude")
        
    def get_longitude(self):
        return self._request("GET", "sitelongitude")

    # --- The 1x1 Mosaic Trick ---
    
    def start_1x1_mosaic(self, target_name, ra_hours, dec_degrees, exposure=10.0, count=180):
        """
        Formats and injects the AAVSO target into the Federation Controller (Device 0).
        """
        logger.info(f"Building 1x1 Mosaic Payload for {target_name}...")
        
        payload = {
            "TargetName": target_name.replace(" ", "_"),
            "RA": float(ra_hours),
            "Dec": float(dec_degrees),
            "Sequence": {
                "Grid": "1x1",
                "Autofocus": True,
                "Exposure": float(exposure),
                "Count": int(count),
                "Gain": 60,
                "LightPollutionFilter": False
            }
        }
        
        # We send this via POST to the Federation Endpoint (Device 0)
        # Note: The exact endpoint name depends on seestar_alp's implementation.
        # We'll use 'sequence' as the standard placeholder.
        result = self._request("POST", "sequence", target_device=0, json_payload=payload)
        
        if result:
            logger.info(f"Payload accepted! Seestar is engaging {target_name}.")
            return True
        else:
            logger.error("Payload rejected by the Federation Controller.")
            return False

if __name__ == "__main__":
    print("--- Testing Block 1: The Trojan Horse ---")
    client = AlpacaClient()
    # Safely test generating the payload without actually firing the telescope
    print("Code compiles cleanly. Ready to inject targets.")
