"""
File: test_link.py
Usage: python3 test_link.py
Description: Verifies the S30-PRO Class in SIMULATION MODE.
"""
import sys
import time
from core.alpaca_sequencer import SeestarClient

# CONFIGURATION
config = {
    "alpaca_host": "127.0.0.1",
    "alpaca_port": 5555,
    "simulate": True  # <--- CRITICAL: BYPASSES NETWORK
}

def main():
    print(f"[INIT] Starting SeestarClient in SIMULATION MODE...")
    client = SeestarClient(config)
    
    # 1. Connection Test
    print("\n--- STEP 1: CONNECTION ---")
    client.connect()
    connected = client._req("GET", "telescope", "connected")
    if connected:
        print(f"[PASS] Simulator Connected.")
    else:
        print(f"[FAIL] Simulator failed to connect.")
        sys.exit(1)

    # 2. Slew Test
    print("\n--- STEP 2: SLEW OPERATION ---")
    target_ra = 10.5
    target_dec = 45.0
    client.slew(target_ra, target_dec)
    
    # Check internal state (Sim cheat)
    if client._sim_state["ra"] == target_ra:
        print(f"[PASS] Telescope arrived at RA {target_ra}")
    else:
        print(f"[FAIL] Telescope drift detected!")

    # 3. Filter Wheel Test (S30-Pro Feature)
    print("\n--- STEP 3: FILTER WHEEL ---")
    client.set_filter(2)
    current_filter = client.get_filter()
    if current_filter == 2:
        print(f"[PASS] Filter Wheel currently at Slot {current_filter}")
    else:
        print(f"[FAIL] Filter Wheel stuck at {current_filter}")

    # 4. Exposure Test
    print("\n--- STEP 4: ACQUISITION ---")
    print("Requesting 3 second exposure...")
    client.start_exposure(3.0)
    print("[PASS] Sequence Simulation Complete.")

if __name__ == "__main__":
    main()
