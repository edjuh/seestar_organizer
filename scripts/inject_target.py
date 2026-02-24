import requests
import json
import time

def wake_and_inject(target_name, ra, dec, device_num=1):
    base_url = f"http://127.0.0.1:5555/api/v1/telescope/{device_num}"
    common_data = {"ClientID": 1, "ClientTransactionID": 2115}

    # 1. Conversion
    alp_ra = ra.replace(':', 'h', 1).replace(':', 'm', 1) + 's'
    alp_dec = dec.replace(':', 'd', 1).replace(':', 'm', 1) + 's'

    # 2. Parameters with Mandatory Keys to avoid KeyErrors 
    params = {
        "target_name": target_name,
        "ra": alp_ra,
        "dec": alp_dec,
        "is_j2000": True,
        "session_time_sec": 3600,
        "is_use_lp_filter": False,  # Mandatory key
        "is_use_autofocus": True,   # Mandatory key 
        "ra_num": 1,
        "dec_num": 1,
        "gain": 80
    }

    payload = {**common_data, "Action": "start_mosaic", "Parameters": json.dumps(params)}
    
    print(f"🚀 Post-Reboot Injection for {target_name}...")
    response = requests.put(f"{base_url}/action", data=payload)
    print(f"📡 Result: {response.text}")

if __name__ == "__main__":
    # Wait for bridge to stabilize before running this manually after reboot
    wake_and_inject("000-BBJ-536", "05:32:41.35", "-01:35:30.6")
