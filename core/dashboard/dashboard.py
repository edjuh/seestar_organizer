"""
Objective: Terminal User Interface (TUI) for real-time system monitoring.
"""
"""
Filename: core/dashboard.py
Usage: dashboard.refresh()
Note: Optimized for 'screen' sessions to provide high-glanceability status.
"""
import os
from datetime import datetime

class Dashboard:
    def __init__(self):
        pass

    def refresh(self, status_data):
        os.system('clear')
        print("="*60)
        print(f"🔭 S30-PRO | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        # Dynamic status printing based on status_data dictionary
        print(f"\n[ SYSTEM STATE ]: {status_data.get('state', 'UNKNOWN')}")
        print(f"[ STORAGE ]: {status_data.get('storage', '??')}")
        print(f"[ WEATHER ]: {status_data.get('weather', '??')}")
        print("="*60)

dashboard = Dashboard()
