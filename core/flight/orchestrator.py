#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: core/flight/orchestrator.py
Version: 1.2.0 (Pee Pastinakel)
Objective: Primary flight control daemon that manages hardware states (Slewing, Centering, Integrating) and broadcasts telemetry to the dashboard.
"""

import os
import sys
import json
import time
import logging

# Ensure core access
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from core.flight.vault_manager import VaultManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')
logger = logging.getLogger("Orchestrator")

class Orchestrator:
    def __init__(self):
        self.vault = VaultManager()
        self.state_file = os.path.expanduser("~/seestar_organizer/core/flight/data/system_state.json")
        
        storage = self.vault.data.get('storage', {})
        self.usb_path = storage.get('primary_dir', '/mnt/usb_buffer')
        self.lifeboat_path = os.path.expanduser(storage.get('lifeboat_dir', '~/seestar_organizer/data/local_buffer'))
        self.active_storage = self._resolve_storage()

    def _resolve_storage(self):
        if os.path.exists(self.usb_path) and os.access(self.usb_path, os.W_OK):
            return self.usb_path
        else:
            os.makedirs(self.lifeboat_path, exist_ok=True)
            return self.lifeboat_path

    def update_dashboard(self, status, target="None", message=""):
        state = {
            "status": status,
            "target": target,
            "message": message,
            "timestamp": time.time()
        }
        with open(self.state_file, 'w') as f:
            json.dump(state, f)

    def execute_plan(self):
        plan_path = os.path.expanduser("~/seestar_organizer/data/tonights_plan.json")
        with open(plan_path, 'r') as f:
            targets = json.load(f)

        logger.info(f"🚀 STARTING MISSION SIMULATION: {len(targets)} Targets.")

        for target in targets:
            name = target['name']
            self.update_dashboard("🛰️ SLEWING", name, f"Moving to RA:{target['ra']} Dec:{target['dec']}")
            time.sleep(3)
            self.update_dashboard("🎯 CENTERING", name, "Plate-solving FOV...")
            time.sleep(2)
            self.update_dashboard("📸 INTEGRATING", name, f"Capture: {target['frames']} x {target['exposure_sec']}s")
            time.sleep(5)
            self.update_dashboard("💾 SYNCING", name, f"Transferring FITS to {os.path.basename(self.active_storage)}")
            time.sleep(2)

        self.update_dashboard("🅿️ PARKED", "OFF-DUTY", "Mission Complete. All targets processed.")
        logger.info("🏁 MISSION COMPLETE.")

if __name__ == "__main__":
    engine = Orchestrator()
    engine.execute_plan()
