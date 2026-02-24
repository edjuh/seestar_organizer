"""
Filename: scripts/status_ticker.py
Objective: Authenticated mission monitoring for Williamina (v1.0 Kwetal).
"""
import requests
import time
import sys

def get_stats(device_num=1):
    base_url = f"http://127.0.0.1:5555/api/v1/telescope/{device_num}/action"
    
    # Authenticated payload for the scheduler specialist
    payload = {
        "Action": "get_event_state",
        "Parameters": "{}",
        "ClientID": 1,
        "ClientTransactionID": 2300
    }
    
    try:
        response = requests.put(base_url, data=payload, timeout=3)
        if response.status_code == 200:
            data = response.json().get("Value", {})
            sched_state = data.get("state", "Unknown")
            is_stacking = data.get("is_stacking", False)
            
            # Mission Ticker Output
            timestamp = time.strftime('%H:%M:%S')
            status_icon = "🔭" if is_stacking else "⏳"
            print(f"[{timestamp}] Scheduler: {sched_state} | Stacking: {status_icon} | Target: V1159 Ori")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] ⚠️  Bridge Error: {response.status_code}")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] ❌ Ticker Lost: {e}")

if __name__ == "__main__":
    print("--- 🛰️ Williamina Specialist Ticker (Ctrl+C to stop) ---")
    while True:
        get_stats()
        time.sleep(60)
