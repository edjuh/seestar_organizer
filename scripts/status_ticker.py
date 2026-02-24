import requests
import time
import os

def get_dashboard():
    # 1. Alpaca/Federation Check
    base = "http://127.0.0.1:5555/api/v1/telescope"
    auth = "ClientID=1&ClientTransactionID=2500"
    
    # 2. Joost Heartbeat (Last line of log)
    try:
        with open("/home/ed/seestar_organizer/logs/seestar_joost.log", "r") as f:
            joost_line = f.readlines()[-1].strip()
    except:
        joost_line = "Log inaccessible"

    try:
        # Pull Alpaca State
        r = requests.put(f"{base}/1/action", data={"Action": "get_event_state", "Parameters": "{}", "ClientID": 1, "ClientTransactionID": 2501}, timeout=1)
        state = r.json().get("Value", {}).get("state", "OFFLINE")
        
        # Dashboard Console Output
        print("-" * 60)
        print(f"[{time.strftime('%H:%M:%S')}] --- 🔭 SEESTAR MISSION CONTROL ---")
        print(f"🏛️  FEDERATION:  ACTIVE (Port 5555)")
        print(f"📡 WILLIAMINA:  {state}")
        print(f"🛡️  JOOST:       {joost_line[25:]}") # Clean up timestamp
        print(f"🌡️  WEATHER:     SAFE (Forced)")
        print(f"🎯 TARGET:      V1159 Ori (000-BBJ-536)")
        print("-" * 60)
    except:
        print(f"[{time.strftime('%H:%M:%S')}] ⚠️ Dashboard: Waiting for Alpaca...")

if __name__ == "__main__":
    while True:
        get_dashboard()
        time.sleep(30)
