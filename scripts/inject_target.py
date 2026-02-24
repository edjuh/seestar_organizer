"""
Filename: scripts/inject_target.py
Objective: Inject targets directly into the Alpaca API (Port 5555) for Williamina.
"""
import requests
import sys

def inject_alpaca(target_name, ra, dec, device_num=1):
    # Standard Alpaca Transaction URL
    url = f"http://127.0.0.1:5555/api/v1/telescope/{device_num}/action"
    
    # Alpaca expects parameters as Form-Data
    payload = {
        "Action": "schedule",
        "Parameters": f'{{"target_name": "{target_name}", "ra": "{ra}", "dec": "{dec}", "is_j2000": true}}',
        "ClientTransactionID": 1234
    }
    
    print(f"🚀 Direct Alpaca Injection for {target_name} (Device {device_num})...")
    
    try:
        response = requests.put(url, data=payload, timeout=5)
        if response.status_code == 200:
            result = response.json()
            if result.get("ErrorNumber") == 0:
                print(f"✅ Success: {target_name} accepted by Alpaca Server.")
            else:
                print(f"❌ Alpaca Error: {result.get('ErrorMessage')}")
        else:
            print(f"❌ Server Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection Failure: {e}")

if __name__ == "__main__":
    # Coronating V1159 Ori for 21:00
    inject_alpaca("000-BBJ-536", "05:32:41.35", "-01:35:30.6", device_num=1)
