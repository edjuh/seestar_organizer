"""
Filename: utils/update_from_targettool.py
Version: 4.2.0 (VSP Integration & Rate-Limit Safe)
Purpose: Fetches targets, removes duplicates, and pulls VSP comparison stars 
         for the top 20 targets to prevent AAVSO API rate limiting.
"""
import requests
import json
import tomllib
import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CONFIG_PATH = BASE_DIR / "config.toml"
DATA_DIR = BASE_DIR / "data"

try:
    with open(CONFIG_PATH, "rb") as f:
        CONFIG = tomllib.load(f)
except Exception as e:
    print(f"[-] FATAL: Could not read config.toml! {e}")
    exit(1)

AAVSO_ID = CONFIG.get("aavso", {}).get("observer_id", "")
AAVSO_TOKEN = CONFIG.get("aavso", {}).get("webobs_token", "")
TARGET_KEY = CONFIG.get("aavso", {}).get("target_tool_key", "")
LAT = CONFIG.get("location", {}).get("lat", 52.38)
LON = CONFIG.get("location", {}).get("lon", 4.64)
MIN_ALT = CONFIG.get("location", {}).get("min_alt", 20)

MAX_MAGNITUDE_LIMIT = 11.0 
TARGET_URL = "https://targettool.aavso.org/TargetTool/api/v1/targets"

def get_v_mag(comp_star):
    for band_data in comp_star.get('bands', []):
        if band_data.get('band') == 'V':
            return band_data.get('mag')
    return "N/A"

def fetch_vsp_sequence(star_name):
    if not AAVSO_ID or not AAVSO_TOKEN:
        return []

    safe_name = urllib.parse.quote(star_name)
    vsp_url = f"https://www.aavso.org/apps/vsp/api/chart/?star={safe_name}&fov=60&maglimit=15&format=json"
    headers = {
        'User-Agent': f'SeestarAutonomy/1.0 (Observer: {AAVSO_ID})',
        'Authorization': f'Bearer {AAVSO_TOKEN}'
    }
    
    try:
        res = requests.get(vsp_url, headers=headers, timeout=10)
        res.raise_for_status()
        return res.json().get('photometry', [])
    except requests.exceptions.RequestException:
        return []

def fetch_and_build():
    print(f"[*] Contacting AAVSO Target Tool...")
    params = {
        'observable': 'true',
        'latitude': LAT,
        'longitude': LON,
        'targetaltitude': MIN_ALT,
        'obs_section': ['ac', 'cv']
    }
    
    try:
        response = requests.get(TARGET_URL, auth=(TARGET_KEY, "api_token"), params=params, timeout=15)
        response.raise_for_status()
        raw_targets = response.json().get('targets', [])
    except requests.exceptions.RequestException as e:
        print(f"[-] API Request Failed: {e}")
        return

    processed_targets = []
    seen_names = set()
    
    for t in raw_targets:
        name = t.get('star_name', 'Unknown')
        if name in seen_names: continue
            
        max_mag = t.get('max_mag')
        if max_mag is None or max_mag > MAX_MAGNITUDE_LIMIT: continue
            
        processed_targets.append({
            "name": name,
            "ra": round(t.get('ra', 0.0) / 15.0, 5),
            "dec": round(t.get('dec', 0.0), 5),
            "priority": 1 if t.get('priority') else 2,
            "mag": max_mag,
            "type": t.get('var_type', 'Variable'),
            "comp_stars": [] # Default empty list
        })
        seen_names.add(name)
    
    # Sort so High Priority is at the top
    processed_targets.sort(key=lambda x: x['priority'])
    
    print(f"[+] Found {len(processed_targets)} capable targets. Fetching VSP for Top 20...")
    
    # Only fetch VSP for the first 20 targets to protect the AAVSO rate limit
    for t in processed_targets[:20]:
        print(f"    -> Pulling VSP chart for {t['name']}...")
        comps = fetch_vsp_sequence(t['name'])
        
        valid_comps = []
        for c in comps:
            v_mag = get_v_mag(c)
            if v_mag != "N/A":
                valid_comps.append({"label": c.get('label'), "v_mag": v_mag})
        
        t['comp_stars'] = valid_comps
    
    filepath = DATA_DIR / "priority.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(processed_targets, f, indent=2)
        
    print(f"\n[+] SUCCESS: Engine is loaded and ready for the night.")

if __name__ == "__main__":
    fetch_and_build()
