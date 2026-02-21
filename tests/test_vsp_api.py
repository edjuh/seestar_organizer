import requests
import json

def test_vsp_sequence():
    url = "https://apps.aavso.org/vsp/api/chart/"
    params = {"star": "CH Cyg", "fov": 60, "maglimit": 14, "format": "json"}
    
    try:
        r = requests.get(url, params=params, timeout=45)
        if r.status_code == 200:
            photometry = r.json().get("photometry", [])
            if photometry:
                print("🌟 Raw Comparison Star JSON:")
                print(json.dumps(photometry[0], indent=2))
    except Exception as e:
        print(f"❌ Network Error: {e}")

if __name__ == "__main__":
    test_vsp_sequence()
