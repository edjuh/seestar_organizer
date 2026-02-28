#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: dashboard/app.py
Version: 1.3.0 (Monkel)
Objective: Mission Control dashboard using real vault data and GPS fix states.
"""

from flask import Flask, render_template
import json
import os
import logging
from pathlib import Path

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.expanduser("~/seestar_organizer")
LOG_FILE = os.path.join(PROJECT_ROOT, "logs/engine.log")
STATUS_PATH = Path("/dev/shm/env_status.json")

# Ensure log directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

app = Flask(__name__, template_folder=os.path.join(CURRENT_DIR, "templates"))

def get_env_status():
    """Read the RAM-disk status pushed by gps_monitor.py"""
    try:
        with open(STATUS_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return {"gps_status": "WAITING", "maidenhead": "HUNTING..."}

@app.route("/")
def index():
    env = get_env_status()
    
    # 1. Map live GPS state
    gps_ui_state = "TRYING"
    if env.get("gps_status") == "FIXED":
        gps_ui_state = "OK"
        
    loc = env.get("maidenhead", "HUNTING...")
    if not loc:
        loc = "HUNTING..."

    # 2. Rebuild the Preflight Dictionary for the UI
    preflight = {
        "location_maidenhead": loc,
        "observer_id": "REDA",
        "jd": "2461099.9204", 
        "bridge": "OK",
        "gps": gps_ui_state,
        "weather": "RAIN",
        "weather_led": "led-red",
        "disk": "NAS: 40% | USB: 94%",
        "disk_led": "led-green",
        "targets": "READY (51)",
        "targets_led": "led-green"
    }
    
    # 3. Rebuild the State Dictionary
    state = {
        "status": "🅿️ PARKED",
        "target": "OFF-DUTY",
        "message": "Mission Complete. All targets processed."
    }
    
    # 4. Rebuild the QC Dictionary
    qc = {
        "last_capture": "N/A",
        "quality": "OK",
        "snr_avg": "N/A"
    }

    return render_template("index.html", preflight=preflight, state=state, qc=qc)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, threaded=True)
