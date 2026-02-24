import time
import os
from core.weather import weather
from core.ephemeris import observer
from core.selector import selector
from core.alpaca_client import alpaca
from core.logger import log_event

def verify_inventory():
    """Check if we have targets to work with before starting."""
    vault_path = "data/sequences/"
    if not os.path.exists(vault_path):
        log_event(f"CRITICAL: Vault path {vault_path} missing!", level="error")
        return 0
    
    count = len([f for f in os.listdir(vault_path) if f.endswith('.json')])
    log_event(f"Inventory: Found {count} object JSONs in vault.")
    return count

def run_cycle():
    # Load simulation and override flags
    sim_mode = os.getenv("SIMULATION_MODE", "False").lower() == "true"
    dark_mode = os.getenv("DARKNESS_OVERRIDE", "False").lower() == "true"
    
    log_event(f"Kwetal: Cycle start (Sim: {sim_mode}, Dark: {dark_mode})")

    # 1. Weather Gate
    if sim_mode:
        log_event("Kwetal: SIMULATION ACTIVE - Ignoring real weather.")
    else:
        if not weather.is_safe_to_image():
            log_event("Kwetal: Weather UNSAFE. Commanding Lockdown.")
            alpaca.park_telescope()
            return

    # 2. Solar Gate
    is_dark = observer.is_dark_enough()
    if not (sim_mode or dark_mode or is_dark):
        log_event(f"Kwetal: Sun is at {observer.sun_alt:.1f}°. Waiting for darkness.")
        return 
    elif sim_mode:
         log_event(f"Kwetal: SIMULATION ACTIVE - Ignoring Sun at {observer.sun_alt:.1f}°.")

    # 3. Priority Target Selection (Westward-First)
    plan = selector.get_night_plan()
    if plan:
        target = plan[0]  # Top priority is the first in the sorted list
        log_event(f"Kwetal: Selected priority target {target['display_name']} at {target['alt']:.1f}° (Az: {target['az']:.1f}°).")
        alpaca.start_observation(target)
    else:
        log_event("Kwetal: No valid targets found in current sky window.")

def main():
    log_event("Kwetal Sentry: Initializing...")
    
    if verify_inventory() == 0:
        log_event("CRITICAL: No targets found. Exiting.", level="error")
        return

    while True:
        try:
            run_cycle()
        except Exception as e:
            log_event(f"Kwetal: Runtime Error: {e}", level="error")
        
        log_event("Kwetal: Cycle complete. Sleeping for 10 minutes.")
        time.sleep(600)

if __name__ == "__main__":
    main()
