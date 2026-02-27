#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Seestar Organizer - Federation ACARS Overseer (Dynamic v1.1)
# Path: ~/seestar_organizer/dashboard/app.py
# Purpose: Mission Control dashboard using real vault data and GPS fix states.
# ----------------------------------------------------------------

from flask import Flask, render_template
import json
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(CURRENT_DIR, "templates")

PREFLIGHT_FILE = os.path.expanduser("~/seestar_organizer/core/flight/data/preflight_status.json")
STATE_FILE = os.path.expanduser("~/seestar_organizer/core/flight/data/system_state.json")
QC_REPORT = os.path.expanduser("~/seestar_organizer/core/postflight/data/qc_report.json")

app = Flask(__name__, template_folder=TEMPLATE_DIR)

def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except: return default
    return default

@app.route("/")
def index():
    preflight = load_json(PREFLIGHT_FILE, {
        "bridge": "BAD", "gps": "BAD", "weather": "BLUE", 
        "location_maidenhead": "------", "observer_id": "UNKNOWN", "jd": 0.0
    })
    state = load_json(STATE_FILE, {"status": "STOPPED", "target": "OFF-DUTY", "message": "No Active Mission"})
    qc = load_json(QC_REPORT, {"last_capture": "None", "quality": "N/A", "frames_valid": 0, "snr_avg": 0.0})

    # Global status color mapping
    status_map = {"IMAGING": "#27ae60", "SLEWING": "#f39c12", "ERROR": "#c0392b", "CALIBRATING": "#8e44ad", "COMPLETE": "#2980b9"}
    bg_color = status_map.get(state.get("status"), "#2c3e50")

    return render_template("index.html", state=state, qc=qc, preflight=preflight, bg_color=bg_color)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
