#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: core/postflight/post_to_pre_feedback.py
Version: 1.2.0 (Pee Pastinakel)
Objective: Updates the master targets.json with successful observation dates extracted from QC reports.
"""

import json
import os
from datetime import datetime

REPORT_PATH = os.path.expanduser("~/seestar_organizer/core/postflight/data/qc_report.json")
TARGETS_PATH = os.path.expanduser("~/seestar_organizer/data/targets.json")

def apply_feedback():
    if not os.path.exists(REPORT_PATH):
        print(f"⚠️ QC Report not found at {REPORT_PATH}")
        return

    with open(REPORT_PATH, 'r') as f:
        qc_results = json.load(f)

    with open(TARGETS_PATH, 'r') as f:
        targets = json.load(f)

    successful_targets = [r['target'] for r in qc_results if r['status'] == "PASS"]
    
    updated_count = 0
    now_str = datetime.now().strftime("%Y-%m-%d")

    for t in targets:
        if t['star_name'] in successful_targets:
            t['last_observed'] = now_str
            updated_count += 1

    with open(TARGETS_PATH, 'w') as f:
        json.dump(targets, f, indent=4)

    print(f"🔄 Feedback Loop Complete: Updated {updated_count} targets in targets.json")

if __name__ == "__main__":
    apply_feedback()
