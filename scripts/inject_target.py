"""
Filename: scripts/inject_target.py
Objective: Authenticated injection of targets into the Federation bridge with response validation.
"""
import requests
import os
import sys

# Ensure core is reachable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def inject(target_name, ra, dec, device_index=1):
    # The SSC endpoint returns HTML, so we must parse it for confirmation
    url = f"http://localhost:5432/{device_index}/schedule"
    payload = {
        "target_name": target_name,
        "ra": ra,
        "dec": dec,
        "is_j2000": True,
        "panel_time_sec": 60
    }
    
    print(f"🚀 Injecting {target_name} into Specialist {device_index} (Williamina)...")
    
    try:
        # We send JSON, but the bridge responds with the full HTML Dashboard
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            # We "catch" the response and look for our AUID in the HTML string
            if target_name in response.text:
                print(f"✅ Success: {target_name} confirmed in the bridge schedule.")
            else:
                print(f"⚠️ Warning: Connection successful, but {target_name} not found in response text.")
        else:
            print(f"❌ Bridge Error: Received status code {response.status_code}")
            
    except Exception as e:
        print(f"❌ Connection Failure: {e}")

if __name__ == "__main__":
    # Handshaking with Williamina for the 21:00 run
    inject("000-BBJ-536", "05:32:41.35", "-01:35:30.6", device_index=1)
