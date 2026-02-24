"""
Filename: scripts/inject_target.py
Objective: Standardized Alpaca injection for Williamina (Device 1) on Port 5555.
"""
import requests
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def inject_alpaca(target_name, ra, dec, device_num=1):
    # Standard Alpaca Action URL
    url = f"http://127.0.0.1:5555/api/v1/telescope/{device_num}/action"
    
    # Payload: Individual fields for the bridge action
    # We pass the parameters as a simple comma-separated or dict string 
    # based on the SSC's specific 'schedule' action handler.
    payload = {
        "Action": "schedule",
        "Parameters": f"name={target_name},ra={ra},dec={dec},j2000=true,panel_time=60",
        "ClientTransactionID": 2100
    }
    
    print(f"🚀 Injecting {target_name} into Alpaca Device {device_num}...")
    
    try:
        # Alpaca uses PUT or POST for state-changing actions
        response = requests.put(url, data=payload, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("ErrorNumber") == 0:
                print(f"✅ Success: {target_name} is locked in.")
            else:
                print(f"❌ Alpaca Refusal: {result.get('ErrorMessage')}")
        else:
            print(f"❌ Server Error {response.status_code}: Bridge rejected the format.")
            print(f"Response: {response.text}") # Show the raw error for debugging
    except Exception as e:
        print(f"❌ Connection Failure: {e}")

if __name__ == "__main__":
    inject_alpaca("000-BBJ-536", "05:32:41.35", "-01:35:30.6", device_num=1)
