import requests
import json

# Beta Pictoris Data
star_name = "Beta Pic"
ra = 88.083
dec = -51.066

def probe(label, url, params):
    print(f"--- Probing {label} ---")
    try:
        r = requests.get(url, params=params, timeout=10)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            print("Success! Data received.")
            # print(json.dumps(r.json(), indent=2)[:200]) # Peek at first 200 chars
        else:
            print(f"Server says: {r.text}")
    except Exception as e:
        print(f"Error: {e}")
    print("\n")

# Probe 1: Full Bayer Name
probe("Full Name", "https://www.aavso.org/apps/vsp/api/chart/", {"star": "Beta Pic", "format": "json"})

# Probe 2: Standard RA/Dec (Fixed FOV/Limit)
probe("Coordinates", "https://www.aavso.org/apps/vsp/api/chart/", {
    "ra": ra, 
    "dec": dec, 
    "fov": 180.0, 
    "maglimit": 15.0, 
    "format": "json"
})

# Probe 3: The 'Star ID' check (if it exists)
probe("Common Name", "https://www.aavso.org/apps/vsp/api/chart/", {"star": "bet Pic", "format": "json"})
