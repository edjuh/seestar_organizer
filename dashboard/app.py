#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: dashboard/app.py
Version: 1.2.0 (Pee Pastinakel)
Objective: Mission Control dashboard using real vault data and GPS fix states; logs routed to central log directory.
"""

from flask import Flask, render_template
import json
import os
import logging

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.expanduser("~/seestar_organizer")
LOG_FILE = os.path.join(PROJECT_ROOT, "logs/engine.log")

# Ensure log directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Configure Flask to log to the central directory instead of root
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

app = Flask(__name__, template_folder=os.path.join(CURRENT_DIR, "templates"))

# ... [rest of the app.py logic preserved] ...

if __name__ == "__main__":
    # Use 'threaded=True' for better performance on Pi 5
    app.run(host="0.0.0.0", port=5050, threaded=True)
