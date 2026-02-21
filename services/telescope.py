#!/usr/bin/env python3
"""
Filename: services/telescope.py
Version: 0.5.5
Description: Enhanced monitoring for Seestar S30-pro via seestar_alp.
"""
import requests
import json
import time
import tomllib
import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(os.getcwd())

class SeestarInterface:
    def __init__(self, config_path="config.toml"):
        self.config_path = Path(config_path)
        self.status_path = Path("logs/telescope_status.json")
        self.load_config()
        
    def load_config(self):
        with open(self.config_path, "rb") as f:
            config = tomllib.load(f)
            conn = config.get("connections", {})
            host = conn.get("seestar_alp_host", "127.0.0.1")
            port = conn.get("seestar_alp_port", 11111)
            self.api_base = f"http://{host}:{port}/api/v1/telescope/0"

    def update_status(self, connected, message, ra=None, dec=None):
        status = {
            "last_check": time.strftime('%Y-%m-%d %H:%M:%S'),
            "connected": connected,
            "message": message,
            "ra": ra,
            "dec": dec
        }
        with open(self.status_path, "w") as f:
            json.dump(status, f)

    def check_telescope(self):
        try:
            # Check connection
            resp = requests.get(f"{self.api_base}/connected", timeout=2)
            if resp.status_code == 200 and resp.json().get("Value"):
                # Get RA/Dec if connected
                ra_resp = requests.get(f"{self.api_base}/rightascension", timeout=2)
                dec_resp = requests.get(f"{self.api_base}/declination", timeout=2)
                
                ra = ra_resp.json().get("Value", "N/A")
                dec = dec_resp.json().get("Value", "N/A")
                
                self.update_status(True, "Tracking", ra, dec)
            else:
                self.update_status(False, "Link OK - Scope Disconnected")
        except:
            self.update_status(False, "Seestar Offline")

    def run(self):
        while True:
            self.check_telescope()
            time.sleep(10)

if __name__ == "__main__":
    SeestarInterface().run()
