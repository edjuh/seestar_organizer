#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: utils/inject_location.py
Version: 1.1.0 (Kwetal)
Role: Integrity Tool
Objective: Dynamically synchronizes Bridge/Simulator location using config.toml as the source of truth.
"""
import requests
import time
import toml
from pathlib import Path

def run():
    # Path to the source of truth
    config_path = Path(__file__).parent.parent / "config.toml"
    
    try:
        config = toml.load(config_path)
        # Pulling from the Seestar Initialization section we saw earlier
        lat = config.get('seestar', {}).get('init_lat', 52.3874)
        lon = config.get('seestar', {}).get('init_long', 4.6462)
        bridge_ip = config.get('alpaca', {}).get('host', '127.0.0.1')
        port = config.get('alpaca', {}).get('port', 5555)
    except Exception as e:
        print(f"⚠️ Could not load config.toml, reverting to defaults: {e}")
        lat, lon, bridge_ip, port = 52.3874, 4.6462, "127.0.0.1", 5555

    base_url = f"http://{bridge_ip}:{port}/api/v1/telescope/1"
    client_id = 42
    
    try:
        # Step 1: Force Handshake (Presence Check)
        requests.put(f"{base_url}/connected", data={"Connected": "true", "ClientID": client_id, "ClientTransactionID": int(time.time())}, timeout=5)
        
        # Step 2: Inject Coordinates
        requests.put(f"{base_url}/sitelatitude", data={"SiteLatitude": lat, "ClientID": client_id, "ClientTransactionID": int(time.time())+1}, timeout=5)
        requests.put(f"{base_url}/sitelongitude", data={"SiteLongitude": lon, "ClientID": client_id, "ClientTransactionID": int(time.time())+2}, timeout=5)
        
        print(f"✅ Synchronized Federation to Config Location: {lat}, {lon}")
    except Exception as e:
        print(f"❌ Connection to Bridge failed: {e}")

if __name__ == "__main__":
    run()
