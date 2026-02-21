#!/usr/bin/env python3
"""
Filename: services/organizer.py
Version: 0.4.1
Description: Standalone FITS organizer for AAVSO photometry. 
             Optimized for RPi 5 / StellarMate.
License: MIT
"""

import os
import time
import shutil
import hashlib
import logging
import tomllib
import json
from pathlib import Path
from astropy.io import fits

class SeestarOrganizer:
    def __init__(self, config_path="config.toml"):
        self.config_path = Path(config_path)
        self.status_path = Path("logs/organizer_status.json")
        self.load_config()
        self.setup_logging()
        self.update_status("Starting", "N/A")

    def load_config(self):
        if not self.config_path.exists():
            print(f"CRITICAL: {self.config_path} not found.")
            exit(1)
        with open(self.config_path, "rb") as f:
            config = tomllib.load(f)
            self.source_dir = Path(config["paths"]["source_dir"])
            self.archive_dir = Path(config["paths"]["archive_dir"])
            self.log_dir = Path(config["paths"]["log_dir"])
            self.interval = config["organizer"]["scan_interval"]
            self.use_checksums = config["organizer"]["use_checksums"]
            self.keep_original = config["organizer"]["keep_original"]
            self.extensions = config["organizer"]["extensions"]

    def setup_logging(self):
        self.log_dir.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(self.log_dir / "organizer.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("Organizer")

    def update_status(self, last_action, last_file):
        status = {
            "last_run": time.strftime('%Y-%m-%d %H:%M:%S'),
            "status": last_action,
            "last_file": last_file,
            "pid": os.getpid()
        }
        try:
            with open(self.status_path, "w") as f:
                json.dump(status, f)
        except Exception as e:
            self.logger.error(f"Failed to update status.json: {e}")

    def get_md5(self, file_path):
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def get_metadata(self, file_path):
        try:
            with fits.open(file_path, mode='readonly') as hdul:
                header = hdul[0].header
                obj = str(header.get('OBJECT', 'Unknown')).strip().replace(' ', '_')
                filt = str(header.get('FILTER', 'NoFilter')).strip()
                return obj, filt
        except Exception as e:
            self.logger.error(f"FITS Error {file_path.name}: {e}")
            return "Corrupt", "Unknown"

    def process_file(self, src_path):
        if not self.archive_dir.exists():
            self.logger.error(f"Archive mount {self.archive_dir} missing!")
            self.update_status("Error: NAS Missing", src_path.name)
            return

        obj, filt = self.get_metadata(src_path)
        dest_dir = self.archive_dir / obj / filt
        
        try:
            dest_dir.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            self.logger.error(f"Permission denied creating {dest_dir}. Check NAS perms.")
            self.update_status("Error: Perm Denied", src_path.name)
            return

        dest_path = dest_dir / src_path.name

        if dest_path.exists():
            if self.use_checksums and self.get_md5(src_path) == self.get_md5(dest_path):
                self.logger.info(f"Duplicate {src_path.name} - removing source.")
                if not self.keep_original: src_path.unlink()
                return
            dest_path = dest_dir / f"{src_path.stem}_{int(time.time())}{src_path.suffix}"

        try:
            if self.keep_original:
                shutil.copy2(src_path, dest_path)
            else:
                shutil.move(src_path, dest_path)
            self.logger.info(f"Organized: {src_path.name} -> {obj}/{filt}")
            self.update_status("Active", f"{obj}/{filt}/{src_path.name}")
        except Exception as e:
            self.logger.error(f"Move failed: {e}")
            self.update_status("IO Error", src_path.name)

    def run(self):
        self.logger.info(f"Organizer v0.4.1 active. Monitoring {self.source_dir}")
        try:
            while True:
                if self.source_dir.exists():
                    files = [f for f in self.source_dir.iterdir() if f.suffix.lower() in self.extensions]
                    if not files:
                        self.update_status("Idle", "N/A")
                    for f in files:
                        self.process_file(f)
                else:
                    self.update_status("Error: Source Missing", "N/A")
                time.sleep(self.interval)
        except KeyboardInterrupt:
            self.update_status("Stopped", "N/A")
            self.logger.info("Service stopping...")

if __name__ == "__main__":
    Path("logs").mkdir(exist_ok=True)
    SeestarOrganizer().run()
