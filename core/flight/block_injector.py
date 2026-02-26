#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Seestar Organizer - Flight Block Injector
# Path: ~/seestar_organizer/core/flight/block_injector.py
# ----------------------------------------------------------------
import requests
import json
import os
import sys

BASE_URL = "http://127.0.0.1:5432/0/schedule"
PLAN_FILE = os.path.expanduser("~/seestar_organizer/core/flight/data/tonights_plan.json")
START_TIMES = ["21.10", "21.30", "21.55"]

def inject(target, start):
    requests.post(f"{BASE_URL}/wait-until", data={"local_time": start})
    requests.post(f"{BASE_URL}/startup", data={"polar_align":"off","auto_focus":"on","dark_frames":"off"})
    requests.post(f"{BASE_URL}/image", data={
        "targetName": target['name'], "ra": target['ra'], "dec": target['dec'],
        "useJ2000": "on", "panelTime": "240", "gain": "80", "useLpFilter": "off", "action": "append"
    })
    requests.post(f"{BASE_URL}/startup", data={"polar_align":"off","auto_focus":"off","dark_frames":"on"})

if __name__ == "__main__":
    with open(PLAN_FILE, 'r') as f:
        targets = json.load(f).get('targets', [])[:3]
    requests.post(f"{BASE_URL}/clear")
    for i, t in enumerate(targets):
        inject(t, START_TIMES[i])
    print("✨ v1.0 Flight Plan Injected.")
