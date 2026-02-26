#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: utils/inject_location.py
Version: 1.0.0 (Kwetal)
Role: Integrity Tool
Objective: Synchronize Bridge and Simulator location to Haarlem (52.3874, 4.6462) to ensure Mosaic accuracy.
"""
import requests
import time

def run():
    base_url = "http://127.0.0.1:5555/api/v1/telescope/1"
    # Logic: Connect -> Inject Lat -> Inject Lon
    requests.put(f"{base_url}/connected", data={"Connected": "true", "ClientID": 42, "ClientTransactionID": int(time.time())})
    requests.put(f"{base_url}/sitelatitude", data={"SiteLatitude": 52.3874, "ClientID": 42, "ClientTransactionID": int(time.time())+1})
    requests.put(f"{base_url}/sitelongitude", data={"SiteLongitude": 4.6462, "ClientID": 42, "ClientTransactionID": int(time.time())+2})
    print("Haarlem coordinates injected into Alpaca Federation.")

if __name__ == "__main__":
    run()
