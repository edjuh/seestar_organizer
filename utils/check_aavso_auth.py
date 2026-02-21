import requests
import os

def get_env_key(key_name):
    if not os.path.exists(".env"): return None
    with open(".env", "r") as f:
        for line in f:
            if line.startswith(key_name):
                return line.strip().split("=")[1].strip('"')

def check_aavso_target_tool():
    api_key = get_env_key("AAVSO_TARGET_KEY")
    if not api_key:
        print("❌ Error: AAVSO_TARGET_KEY not found in .env")
        return

    url = "https://targettool.aavso.org/TargetTool/api/v1/targets"
    
    # We will ask for the Alerts & Campaigns section ("ac") to keep the payload manageable
    params = {
        "obs_section": '["ac"]',
        "observable": "false" # Keep it simple for the auth test
    }
    
    print("Sending Basic Auth request to AAVSO Target Tool...")
    # The crucial fix: Basic Auth (username=KEY, password="api_token")
    r = requests.get(url, params=params, auth=(api_key, "api_token"), timeout=10)
    
    if r.status_code == 200:
        data = r.json()
        targets = data.get("targets", [])
        print(f"✅ AAVSO Auth SUCCESS: 200 OK")
        print(f"✅ Retrieved {len(targets)} targets in the 'Alerts & Campaigns' section.")
        if targets:
            print(f"   Sample Target: {targets[0].get('star_name')} at RA: {targets[0].get('ra')}")
    else:
        print(f"❌ AAVSO Auth FAILED: {r.status_code}")
        print(r.text[:200])

if __name__ == "__main__":
    check_aavso_target_tool()
