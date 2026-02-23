"""
Filename: steward_live.py
Objective: Live Terminal Dashboard for active observation monitoring.
Usage: python3 steward_live.py
Note: The 'face' of Joost. Best viewed in a dedicated terminal or screen.
"""
import time
from core.dashboard import dashboard
from core.orchestrator import orchestrator

def run_live():
    try:
        while True:
            # Aggregate status from components
            status = {
                "state": "OBSERVING" if orchestrator.is_active else "IDLE",
                "weather": "CLEAR" if orchestrator.check_safety() else "DANGER",
                "storage": "NOMINAL"
            }
            dashboard.refresh(status)
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n👋 Steward signing off.")

if __name__ == "__main__":
    run_live()
