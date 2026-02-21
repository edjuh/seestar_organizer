#!/usr/bin/env python3
"""
Filename: services/telescope_service.py
Version: 0.7.1
Role: Bridge between Seestar Alpaca API and Command Center JSON.
"""
import time
import json
import requests
import tomllib
from pathlib import Path

def run_service():
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)
    
    # Standardized status format
    status_path = Path("logs/telescope_status.json")
    conn = config.get("connections", {})
    host = conn.get("seestar_alp_host", "127.0.0.1")
    port = conn.get("seestar_alp_port", 11111)
    
    url = f"http://{host}:{port}/api/v1/telescope/0"

    while True:
        try:
            # We check the Alpaca 'connected' endpoint
            r = requests.get(f"{url}/connected", timeout=5)
            connected = r.json().get("Value", False)
            
            status = {
                "safe": connected,
                "status": "Online" if connected else "Seestar Offline",
                "metrics": {
                    "connected": connected,
                    "ra": "N/A", # Will be updated with v0.7.2 astrometric logic
                    "dec": "N/A"
                }
            }
        except Exception:
            status = {"safe": False, "status": "Seestar Offline", "metrics": {"connected": False}}

        with open(status_path, "w") as f:
            json.dump(status, f)
        
        time.sleep(10)

if __name__ == "__main__":
    run_service()
