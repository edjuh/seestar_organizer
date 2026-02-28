#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Objective: Updates targets.json with successful observation dates.
"""
#
# Seestar Organizer - Post-to-Pre Feedback Loop
# Path: ~/seestar_organizer/core/post_to_pre_feedback.py
# ----------------------------------------------------------------

import json
import os
from datetime import datetime

# Authoritative Paths
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

    # Find targets that earned a "PASS" grade
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
