#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Objective: Stress-test utility to saturate the Federation schedule for maximum night capacity.
"""
#
# Seestar Organizer - Full Night Stress Loader
# Path: ~/seestar_organizer/core/flight/fill_the_night.py
# ----------------------------------------------------------------
import requests
import json
import os
import datetime

BASE_URL = "http://127.0.0.1:5432/0/schedule"
PLAN_FILE = os.path.expanduser("~/seestar_organizer/core/flight/data/tonights_plan.json")
START_TIME = datetime.datetime.strptime("19:30", "%H:%M")
END_TIME = datetime.datetime.strptime("05:30", "%H:%M")

if __name__ == "__main__":
    with open(PLAN_FILE, 'r') as f:
        targets = json.load(f).get('targets', [])
    requests.post(f"{BASE_URL}/clear")
    curr = START_TIME
    while curr < END_TIME or (END_TIME < START_TIME and curr >= START_TIME):
        t = targets[0]
        requests.post(f"{BASE_URL}/wait-until", data={"local_time": curr.strftime("%H.%M")})
        requests.post(f"{BASE_URL}/startup", data={"polar_align":"off","auto_focus":"on","dark_frames":"off"})
        curr += datetime.timedelta(minutes=15)
        if curr >= datetime.datetime.strptime("23:59", "%H:%M") and END_TIME < START_TIME:
            pass # Continue logic for day-roll
    print(f"✨ v1.0 Night Fully Booked.")
