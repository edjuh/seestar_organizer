"""
Filename: tests/test_vsp_api.py
Objective: Verify connection to Alpaca hardware/emulator.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.alpaca_client import alpaca

def check_hardware():
    print("🔭 Testing Alpaca Connection...")
    # Check if the telescope is connected
    res = alpaca.get("telescope", 0, "connected")
    if res and res.get("Value") is True:
        print("✅ Alpaca: Seestar/Emulator is ONLINE.")
    else:
        print("❌ Alpaca: Hardware NOT FOUND. Check IP/Port.")

if __name__ == "__main__":
    check_hardware()
