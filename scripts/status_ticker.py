"""
Filename: scripts/status_ticker.py
Objective: Authenticated monitoring of Williamina's 21:00 mission.
"""
import requests
import time
import sys

def get_vitals(device_num=1):
    base_url = f"http://127.0.0.1:5555/api/v1/telescope/{device_num}"
    # Using the discovery parameters we validated
    auth = "ClientID=1&ClientTransactionID=2205"
    
    try:
        # Check the Action-based state via the Federation or Device
        payload = {"Action": "get_event_state", "Parameters": "{}", "ClientID": 1, "ClientTransactionID": 2206}
        response = requests.put(f"{base_url}/action", data=payload, timeout=2)
        
        if response.status_code == 200:
            val = response.json().get("Value", {})
            state = val.get("state", "Unknown")
            item = val.get("item_number", "N/A")
            
            # Print a clean line for the ticker
            print(f"[{time.strftime('%H:%M:%S')}] Williamina: {state} | Item: {item} | 21:00 Goal: V1159 Ori")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] ⚠️ API Polling Error: {response.status_code}")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] ❌ Ticker Lost Connection: {e}")

if __name__ == "__main__":
    print("--- 🔭 Williamina 21:00 Mission Watch (Ctrl+C to stop) ---")
    while True:
        get_vitals()
        time.sleep(60)
