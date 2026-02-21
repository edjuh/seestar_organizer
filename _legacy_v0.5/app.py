#!/usr/bin/env python3
"""
Filename: app.py
Project: Seestar Organizer v0.4.1
Description: Core application logic and environment validation.
"""

import tomllib
import os
from pathlib import Path
from core.weather import WeatherMonitor # Ensure this matches core/weather.py

class SeestarApp:
    def __init__(self, config_path="config.toml"):
        self.config_path = Path(config_path)
        self.load_config()
        # Initialize weather from the config dict
        self.weather = WeatherMonitor(self.config.get("weather", {}))
        
    def load_config(self):
        if not self.config_path.exists():
            print(f"CRITICAL: {self.config_path} not found.")
            exit(1)
        with open(self.config_path, "rb") as f:
            self.config = tomllib.load(f)
            
        self.source_dir = Path(self.config["paths"]["source_dir"])
        self.archive_dir = Path(self.config["paths"]["archive_dir"])

    def initialize(self):
        """Pre-flight check for sysadmin sanity."""
        if not os.access(self.archive_dir, os.W_OK):
            if not os.access(self.archive_dir.parent, os.W_OK):
                print(f"WARNING: No write access to {self.archive_dir.parent}")
        
        Path(self.config["paths"]["log_dir"]).mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    app = SeestarApp()
    app.initialize()
