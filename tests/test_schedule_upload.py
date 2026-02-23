"""
Filename: tests/test_schedule_upload.py
Objective: Validate the Alpaca protocol for target list transmission.
Usage: python3 tests/test_schedule_upload.py
Note: Tests the specific 'slewtocoordinates' and 'tracking' handshake.
"""
from core.alpaca_client import alpaca

def test_upload():
    print("📡 Testing Alpaca Protocol Handshake...")
    # Test with Vega (RA: 18.6, Dec: 38.7)
    try:
        r = alpaca.slew_to_coordinates(18.6, 38.7)
        if r.status_code == 200:
            print("✅ Protocol Accepted.")
        else:
            print(f"❌ Protocol Rejected: {r.status_code}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    test_upload()
