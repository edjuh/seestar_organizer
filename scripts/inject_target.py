"""
Filename: scripts/inject_target.py
Objective: Authenticated injection of targets into the Federation bridge with response validation.
"""
import requests
import sys

def inject(target_name, ra, dec, device_index=1):
    url = f"http://localhost:5432/{device_index}/schedule"
    payload = {
        "target_name": target_name,
        "ra": ra,
        "dec": dec,
        "is_j2000": True,
        "panel_time_sec": 60
    }
    
    print(f"🚀 Injecting {target_name} into Device {device_index}...")
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        
        # Check if the injection was successful
        if response.status_code == 200:
            # Look for the target name in the returned HTML to confirm it's in the list
            if target_name in response.text:
                print(f"✅ Success: {target_name} is now in the bridge queue.")
            else:
                print(f"⚠️ Warning: Request sent, but {target_name} not found in UI response.")
        else:
            print(f"❌ Failed: Bridge returned status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: Could not connect to the bridge: {e}")

if __name__ == "__main__":
    # Test with Williamina's 21:00 target
    inject("000-BBJ-536", "05:32:41.35", "-01:35:30.6", device_index=1)
