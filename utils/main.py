"""
Filename: main.py
Objective: Final Phase 1.4 Orchestrator - Hardware & Horizon Aware.
"""
import time
import os
from core.weather import weather
from core.ephemeris import observer
from core.selector import selector
from core.alpaca_client import alpaca
from core.hardware_profiles import get_config
from core.logger import log_event

def run_cycle():
    # Load Hardware Identity
    model = os.getenv("SEESTAR_MODEL", "S30_PRO")
    hw = get_config(model)
    
    log_event(f"Kwetal: Cycle start. Monitoring for {model}...")

    # 1. Weather Safety (The Shield)
    if not weather.is_safe_to_image():
        log_event("Kwetal: Weather UNSAFE. Commanding Park/Shutdown.")
        alpaca.park_telescope()
        return

    # 2. Solar Safety (The Gate)
    if not observer.is_dark_enough():
        log_event("Kwetal: Sun is active. Standing by for Nautical Twilight.")
        # return # Keep commented for simulation/testing

    # 3. Target Selection (The Brain)
    # The Selector now automatically uses Horizon Masking and Altitude sorting
    target = selector.get_best_target()
    
    if not target:
        log_event("Kwetal: No targets clear the horizon/obstructions right now.")
        return

    # 4. Hardware Command (The Muscle)
    log_event(f"Kwetal: Best valid target: {target['name']} at {target['current_alt']:.1f}°.")
    
    # In a real run, we would send this to the Alpaca Bridge
    success = alpaca.start_observation(target)
    
    if success:
        log_event(f"Kwetal: Mission {target['name']} successfully queued on {model}.")

def main():
    log_event("Kwetal Daemon: Active and Guarding the Skies.")
    while True:
        try:
            run_cycle()
        except Exception as e:
            log_event(f"Kwetal: Critical Loop Error: {e}", level="error")
        
        log_event("Kwetal: Sleeping for 10 minutes.")
        time.sleep(600)

if __name__ == "__main__":
    main()
