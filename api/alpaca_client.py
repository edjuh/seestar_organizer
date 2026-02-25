#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import logging

# Set up local logging for this block
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger("AlpacaClient")

class AlpacaClient:
    """Block 1: The exclusive communicator for the Seestar Alpaca API."""
    
    def __init__(self, host="127.0.0.1", port=5555, device_number=1, client_id=1):
        self.base_url = f"http://{host}:{port}/api/v1/telescope/{device_number}"
        self.client_id = client_id
        self.transaction_id = 1
        self.timeout = 3  # Strict timeout so the app never hangs

    def _get_auth_params(self):
        self.transaction_id += 1
        return {"ClientID": self.client_id, "ClientTransactionID": self.transaction_id}

    def _request(self, method, endpoint, data=None):
        """Centralized request handler with hardened error catching."""
        url = f"{self.base_url}/{endpoint}"
        params = self._get_auth_params()
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, params=params, timeout=self.timeout)
            elif method.upper() == "PUT":
                # PUT requests need auth in the form data
                payload = {**params}
                if data:
                    payload.update(data)
                response = requests.put(url, data=payload, timeout=self.timeout)
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()
            result = response.json()
            
            if result.get("ErrorNumber", 0) != 0:
                logger.warning(f"Alpaca API Error {result.get('ErrorNumber')}: {result.get('ErrorMessage')}")
                return None
                
            return result.get("Value")

        except requests.exceptions.RequestException as e:
            logger.error(f"Connection failed: {endpoint} -> {e}")
            return None
        except ValueError as e:
            logger.error(f"JSON Parsing failed: {endpoint} -> {e}")
            return None

    # --- Standardized API Methods ---

    def is_connected(self):
        """Returns True if connected to hardware, False otherwise."""
        result = self._request("GET", "connected")
        return bool(result) if result is not None else False

    def get_latitude(self):
        """Returns the current latitude, or None if unavailable."""
        return self._request("GET", "sitelatitude")
        
    def get_longitude(self):
        """Returns the current longitude, or None if unavailable."""
        return self._request("GET", "sitelongitude")


# --- Standalone Self-Test ---
if __name__ == "__main__":
    print("--- Testing Block 1: Alpaca Client ---")
    client = AlpacaClient()
    
    connected = client.is_connected()
    print(f"Connection Status: {connected}")
    
    if connected:
        lat = client.get_latitude()
        lon = client.get_longitude()
        print(f"Latitude:  {lat}")
        print(f"Longitude: {lon}")
    else:
        print("Bridge is not connected to hardware. Cannot read coordinates.")
