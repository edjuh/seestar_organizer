#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Objective: Audits the nightly plan for freshness and quantity.
"""
#
# Seestar Organizer - Target Manifest Evaluator
# Path: ~/seestar_organizer/core/preflight/target_evaluator.py
# ----------------------------------------------------------------

import json
import os
import time
from datetime import datetime

class TargetEvaluator:
    def __init__(self):
        self.base_dir = os.path.expanduser("~/seestar_organizer/data")
        self.observable_path = os.path.join(self.base_dir, "targets/observable_targets.json")
        self.plan_path = os.path.join(self.base_dir, "tonights_plan.json")

    def evaluate(self):
        """Returns {status, led, count}"""
        # 1. Check for the Final Manifest
        if os.path.exists(self.plan_path):
            # Check for freshness (Was it modified today?)
            file_time = os.path.getmtime(self.plan_path)
            if datetime.fromtimestamp(file_time).date() == datetime.now().date():
                try:
                    with open(self.plan_path, 'r') as f:
                        data = json.load(f)
                        count = len(data) if isinstance(data, list) else 0
                        if count > 0:
                            return {"status": f"READY ({count})", "led": "led-green"}
                        else:
                            return {"status": "EMPTY PLAN", "led": "led-red"}
                except Exception:
                    return {"status": "PLAN ERROR", "led": "led-red"}
            else:
                return {"status": "STALE PLAN", "led": "led-orange"}

        # 2. Check if the Filtered list exists but planner hasn't run
        if os.path.exists(self.observable_path):
            return {"status": "NEEDS PLAN", "led": "led-orange"}

        # 3. No data found
        return {"status": "NO TARGETS", "led": "led-red"}

if __name__ == "__main__":
    evaluator = TargetEvaluator()
    print(evaluator.evaluate())
