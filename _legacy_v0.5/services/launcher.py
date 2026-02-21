"""
Filename: services/launcher.py
Version: 0.7.2
Role: Master Supervisor for Organizer, Weather, and AAVSO Target Manager.
"""
import subprocess
import time
import sys
from pathlib import Path

# Ensure we use the venv's python to avoid Skyfield import errors
VENV_PYTHON = str(Path(sys.executable))

SERVICES = [
    [VENV_PYTHON, "-m", "services.organizer_service"],
    [VENV_PYTHON, "-m", "services.weather_safety"],
    [VENV_PYTHON, "services/target_manager.py"]  # This feeds the dashboard
]

processes = []

print(f"[*] Booting Seestar Fleet using {VENV_PYTHON}...")

for cmd in SERVICES:
    try:
        p = subprocess.Popen(cmd)
        processes.append(p)
        print(f"[OK] Started: {' '.join(cmd)}")
        time.sleep(1) 
    except Exception as e:
        print(f"[FAIL] Could not start {cmd}: {e}")

try:
    while True:
        # Check if child processes are still alive
        for p in processes:
            if p.poll() is not None:
                print(f"[!] Process {p.pid} died. Restarting fleet or checking logs...")
        time.sleep(5)
except KeyboardInterrupt:
    print("\n[*] Manual shutdown initiated...")
    for p in processes:
        p.terminate()
