"""
Filename: scripts/inject_target.py
Objective: Inject target into Williamina using the Bruno-validated 'start_mosaic' dialect.
"""
import requests
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def inject_alpaca(target_name, ra, dec, device_num=1):
    url = f"http://127.0.0.1:5555/api/v1/telescope/{device_num}/action"
    
    # 1. Format coordinates to Alpish (hms/dms) 
    # '05:32:41.35' -> '05h32m41.35s'
    # '-01:35:30.6' -> '-01d35m30.6s'
    alp_ra = ra.replace(':', 'h', 1).replace(':', 'm', 1) + 's'
    alp_dec = dec.replace(':', 'd', 1).replace(':', 'm', 1) + 's'

    # 2. Construct the parameters JSON string 
    params = {
        "target_name": target_name,
        "ra": alp_ra,
        "dec": alp_dec,
        "is_j2000": True,
        "session_time_sec": 3600, # 1 hour science run
        "gain": 80
    }

    # 3. Final payload using 'start_mosaic' 
    payload = {
        "Action": "start_mosaic",
        "Parameters": json.dumps(params),
        "ClientID": 1,
        "ClientTransactionID": 2100
    }
    
    print(f"🚀 Injecting {target_name} via 'start_mosaic' to Device {device_num}...")
    
    try:
        response = requests.put(url, data=payload, timeout=5)
        if response.status_code == 200:
            result = response.json()
            if result.get("ErrorNumber") == 0:
                print(f"✅ Success: Williamina accepted the 21:00 mission.")
            else:
                print(f"❌ Refusal: {result.get('ErrorMessage')}")
        else:
            print(f"❌ Server Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Connection Failure: {e}")

if __name__ == "__main__":
    inject_alpaca("000-BBJ-536", "05:32:41.35", "-01:35:30.6", device_num=1)
