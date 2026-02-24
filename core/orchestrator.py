"""
Filename: core/orchestrator.py
Objective: The Kwetal Master Loop. Runs continuously as a systemd daemon.
"""
import sys
import time
from pathlib import Path

# The Kwetal Path Lock
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.weather import weather
from core.alpaca_client import alpaca
from core.logger import log_event

class Orchestrator:
    def __init__(self):
        self.is_running = True
        self.poll_interval = 600  # Wake up every 10 minutes

    def run_night_shift(self):
        log_event("Kwetal Orchestrator: Booting sequence initiated.")
        
        while self.is_running:
            log_event("Kwetal: Waking up for routine check...")
            
            # 1. The Safety Gate
            if not weather.is_safe_to_image():
                log_event("Kwetal: Weather is UNSAFE. Initiating hardware lockdown.")
                alpaca.park_telescope()  # THE MUSCLE WIRE
                self.sleep_cycle()
                continue
                
            # 2. The Target Gate
            log_event("Kwetal: Weather is SAFE. Checking target visibility...")
            
            # 3. The Imaging Loop
            log_event("Kwetal: Target locked. Initiating tracking and imaging...")
            
            self.sleep_cycle()

    def sleep_cycle(self):
        log_event(f"Kwetal: Cycle complete. Sleeping for {self.poll_interval // 60} minutes.")
        try:
            time.sleep(self.poll_interval)
        except KeyboardInterrupt:
            log_event("Kwetal: Manual interrupt detected. Shutting down.")
            self.is_running = False

if __name__ == "__main__":
    master_brain = Orchestrator()
    master_brain.run_night_shift()
