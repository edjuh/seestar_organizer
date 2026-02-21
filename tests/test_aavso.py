import requests
from requests.auth import HTTPBasicAuth

OBS_CODE = "REDA"
TARGET_TOOL_KEY = "deb9c3a2635e14c4ecce2add517e8e30"

def verify_aavso():
    print(f"--- 📋 AAVSO Target Tool Probe: {OBS_CODE} ---")
    url = "https://targettool.aavso.org/TargetTool/api/v1/targets?high_priority=true"
    try:
        # AAVSO API: Username is the API Key, Password is "api_token"
        response = requests.get(url, auth=HTTPBasicAuth(TARGET_TOOL_KEY, "api_token"), timeout=15)
        if response.status_code == 200:
            targets = response.json()
            print(f"✅ SUCCESS! Found {len(targets)} active campaigns.")
            if len(targets) > 0:
                name = targets[0].get('star_name', 'Unknown')
                ra = targets[0].get('ra', 'N/A')
                print(f"   Sample Target: {name} (RA: {ra})")
        else:
            print(f"❌ ERROR {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ SCRIPT ERROR: {e}")

if __name__ == "__main__":
    verify_aavso()
