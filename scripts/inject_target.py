import requests
import json
import time

def check_and_inject(target_name, ra, dec, device_num=1):
    base_url = f"http://127.0.0.1:5555/api/v1/telescope/{device_num}"
    auth = "ClientID=1&ClientTransactionID=2150"
    
    # 1. Check current connection status
    print(f"🕵️ Checking Williamina status...")
    r = requests.get(f"{base_url}/connected?{auth}")
    if not r.json().get("Value"):
        print("📡 Device reports 'False'. Attempting to force connection...")
        requests.put(f"{base_url}/connected", data={"Connected": "true", "ClientID": 1, "ClientTransactionID": 2151})
        time.sleep(3) # Wait for thread init

    # 2. Final Injection with full parameters to avoid KeyErrors
    alp_ra = ra.replace(':', 'h', 1).replace(':', 'm', 1) + 's'
    alp_dec = dec.replace(':', 'd', 1).replace(':', 'm', 1) + 's'
    params = {
        "target_name": target_name, "ra": alp_ra, "dec": alp_dec, "is_j2000": True,
        "is_use_lp_filter": False, "is_use_autofocus": True, "session_time_sec": 3600
    }
    
    print(f"🚀 Injecting {target_name}...")
    resp = requests.put(f"{base_url}/action", data={
        "Action": "start_mosaic", "Parameters": json.dumps(params), 
        "ClientID": 1, "ClientTransactionID": 2152
    })
    print(f"📡 Response: {resp.text}")

if __name__ == "__main__":
    check_and_inject("000-BBJ-536", "05:32:41.35", "-01:35:30.6")
