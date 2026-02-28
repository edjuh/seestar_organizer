#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Objective: Validates FITS headers and calculates basic QC metrics.
"""
#
# Seestar Organizer - Post-Flight Analyst
# Path: ~/seestar_organizer/core/postflight/analyzer.py
# ----------------------------------------------------------------

import os
import sys
import json
import logging
import toml
from astropy.io import fits
import numpy as np

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')
logger = logging.getLogger("Analyst")

class Analyst:
    def __init__(self):
        self.config = self._load_config()
        storage = self.config.get('storage', {})
        # Check Primary, then Lifeboat
        usb = storage.get('primary_dir', '/mnt/usb_buffer')
        lifeboat = os.path.expanduser(storage.get('lifeboat_dir', '~/seestar_organizer/data/local_buffer'))
        
        self.source_path = usb if os.path.exists(usb) and any(f.endswith('.fits') for f in os.listdir(usb)) else lifeboat
        self.report_path = os.path.expanduser("~/seestar_organizer/core/postflight/data/qc_report.json")

    def _load_config(self):
        path = os.path.expanduser("~/seestar_organizer/config.toml")
        return toml.load(open(path))

    def analyze_frame(self, filepath):
        """Extracts metadata and basic SNR from a single FITS file."""
        try:
            with fits.open(filepath) as hdul:
                header = hdul.header
                data = hdul.data
                
                # Metadata extraction
                obj_name = header.get('OBJECT', 'Unknown')
                exp_time = header.get('EXPTIME', 0)
                date_obs = header.get('DATE-OBS', 'N/A')
                
                # Basic SNR Estimation
                # (Simple: Mean of signal / StdDev of background)
                mean_signal = np.mean(data)
                std_bg = np.std(data)
                snr = mean_signal / std_bg if std_bg > 0 else 0
                
                return {
                    "file": os.path.basename(filepath),
                    "target": obj_name,
                    "exposure": exp_time,
                    "timestamp": date_obs,
                    "snr": round(float(snr), 2),
                    "status": "PASS" if snr > 5 else "FAIL" # Scientific floor
                }
        except Exception as e:
            logger.error(f"Error analyzing {filepath}: {e}")
            return None

    def run_batch(self):
        if not os.path.exists(self.source_path):
            logger.warning(f"Source path {self.source_path} not found.")
            return

        fits_files = [f for f in os.listdir(self.source_path) if f.endswith('.fits')]
        logger.info(f"🔍 Analyzing {len(fits_files)} frames in {self.source_path}...")

        results = []
        for f in fits_files:
            report = self.analyze_frame(os.path.join(self.source_path, f))
            if report:
                results.append(report)

        with open(self.report_path, 'w') as f:
            json.dump(results, f, indent=4)
        
        logger.info(f"✅ QC Report generated: {self.report_path}")

if __name__ == "__main__":
    analyst = Analyst()
    analyst.run_batch()
