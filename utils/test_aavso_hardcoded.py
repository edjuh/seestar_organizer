import requests

def test_wire():
    # Hardcoded for the raw test
    api_key = "deb9c3a2635e14c4ecce2add517e8e30"
    url = "https://targettool.aavso.org/TargetTool/api/v1/targets"
    
    # Just grab 5 targets from Alerts & Campaigns to prove it works
    params = {"obs_section": '["ac"]'}
    
    print("Testing AAVSO TargetTool API (Basic Auth)...")
    try:
        r = requests.get(url, params=params, auth=(api_key, "api_token"), timeout=10)
        
        if r.status_code == 200:
            data = r.json()
            targets = data.get("targets", [])
            print(f"✅ SUCCESS: 200 OK. Retrieved {len(targets)} targets.")
            if targets:
                print(f"🌟 First Target: {targets[0].get('star_name')} | RA: {targets[0].get('ra')} | DEC: {targets[0].get('dec')}")
        else:
            print(f"❌ FAILED: Status {r.status_code}")
            print(r.text[:200])
    except Exception as e:
        print(f"❌ FAILED: Network error - {e}")

if __name__ == "__main__":
    test_wire()
