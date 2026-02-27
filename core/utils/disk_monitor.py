#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Seestar Organizer - Universal Disk Monitor
# Path: ~/seestar_organizer/core/utils/disk_monitor.py
# Purpose: Verifies NAS and local USB/buffer storage availability across all flight phases.
# ----------------------------------------------------------------

import os
import shutil
import sys

# Ensure we can reach the VaultManager
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from core.flight.vault_manager import VaultManager

class DiskMonitor:
    def __init__(self):
        self.vault = VaultManager()
        self.storage_cfg = self.vault.data.get("storage", {})
        
        # Pull paths directly from config.toml
        self.nas_dir = self.storage_cfg.get("primary_dir", "/mnt/astro_nas/organized_fits")
        self.usb_dir = self.storage_cfg.get("source_dir", "/home/ed/seestar_downloads")

    def _check_space(self, path):
        """Returns (is_available, percent_free)"""
        if not os.path.exists(path):
            return False, 0.0
        try:
            total, used, free = shutil.disk_usage(path)
            if total == 0:
                return False, 0.0
            return True, (free / total) * 100
        except Exception:
            return False, 0.0

    def check_vitals(self):
        nas_ok, nas_free = self._check_space(self.nas_dir)
        usb_ok, usb_free = self._check_space(self.usb_dir)

        led = "led-green"
        status_text = []

        # Evaluate NAS Capacity
        if not nas_ok:
            led = "led-red"
            status_text.append("NAS: ERR")
        elif nas_free < 5.0:
            led = "led-red"
            status_text.append(f"NAS: {int(nas_free)}%!")
        elif nas_free < 20.0:
            if led != "led-red": led = "led-orange"
            status_text.append(f"NAS: {int(nas_free)}%")
        else:
            status_text.append(f"NAS: {int(nas_free)}%")

        # Evaluate USB/Buffer Capacity
        if not usb_ok:
            led = "led-red"
            status_text.append("USB: ERR")
        elif usb_free < 5.0:
            led = "led-red"
            status_text.append(f"USB: {int(usb_free)}%!")
        elif usb_free < 20.0:
            if led != "led-red": led = "led-orange"
            status_text.append(f"USB: {int(usb_free)}%")
        else:
            status_text.append(f"USB: {int(usb_free)}%")

        final_status = " | ".join(status_text)
        return {"status": final_status, "led": led}

if __name__ == "__main__":
    monitor = DiskMonitor()
    print(monitor.check_vitals())
