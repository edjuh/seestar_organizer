import requests
import json
import time

def wake_and_inject(target_name, ra, dec, device_num=1):
    base_url = f"http://127.0.0.1:5555/api/v1/telescope/{device_num}"
    common_data = {"ClientID": 1, "ClientTransactionID": 2100}

    # 1. Force Connection State
    print(f"📡 Waking Williamina (Device {device_num})...")
    requests.put(f"{base_url}/connected", data={**common_data, "Connected": "true"})
    
    # 2. Handshake Buffer: Give the watch thread time to flip the 'is_connected' flag
    print("⏳ Waiting for handshake stabilization...")
    time.sleep(2) 

    # [cite_start]3. Convert coordinates to Alpish [cite: 21]
    alp_ra = ra.replace(':', 'h', 1).replace(':', 'm', 1) + 's'
    alp_dec = dec.replace(':', 'd', 1).replace(':', 'm', 1) + 's'

    # [cite_start]4. Inject Target via 'start_mosaic' [cite: 21]
    params = {"target_name": target_name, "ra": alp_ra, "dec": alp_dec, "is_j2000": True}
    payload = {**common_data, "Action": "start_mosaic", "Parameters": json.dumps(params)}
    
    print(f"🚀 Injecting {target_name}...")
    response = requests.put(f"{base_url}/action", data=payload)
    
    result = response.json()
    if result.get("ErrorNumber") == 0:
        print(f"✅ Success: {target_name} accepted.")
    else:
        print(f"❌ Refusal: {result.get('ErrorMessage')} (Error {result.get('ErrorNumber')})")

if __name__ == "__main__":
    wake_and_inject("000-BBJ-536", "05:32:41.35", "-01:35:30.6")
