#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Seestar Organizer - Flight Manifest Reporter
# Path: ~/seestar_organizer/core/flight/get_manifest.py
# Purpose: Human-readable reporter for the current Alpaca Bridge flight schedule.
# ----------------------------------------------------------------
import requests

URL = "http://127.0.0.1:5555/api/v1/telescope/0/action"

if __name__ == "__main__":
    try:
        res = requests.put(URL, data={"Action":"get_schedule","Parameters":"{}","ClientID":"1","ClientTransactionID":"999"}, timeout=5)
        items = res.json().get("Value", {}).get("list", [])
        print(f"\n{'TIME':<10} | {'ACTION':<15} | {'TARGET'}")
        print("-" * 50)
        t = "PENDING"
        for i in items:
            if i['action'] == "wait_until": t = i['params']['local_time']
            elif i['action'] == "start_mosaic": print(f"{t:<10} | Science Run     | {i['params']['target_name']}")
            elif i['action'] == "start_up_sequence" and i['params'].get("dark_frames"):
                 print(f"{t:<10} | Dark Calibration| ---")
        print("-" * 50)
    except Exception as e:
        print(f"Error: {e}")
