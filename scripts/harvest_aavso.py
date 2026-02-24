"""
Filename: scripts/harvest_aavso.py
Objective: Automated scraping of AAVSO Alert Notices to populate the observation queue.
"""
"""
Filename: scripts/harvest_aavso.py
Objective: Scrapes the AAVSO target list for new Alert Notices and high-priority events.
"""
import requests
import json
import tomllib
from pathlib import Path

def harvest():
    project_root = Path(__file__).parent.parent
    with open(project_root / "config.toml", "rb") as f:
        config = tomllib.load(f)
    
    api_key = config['aavso']['target_tool_key']
    # The actual functional endpoint for the Target Tool export
    url = f"https://www.aavso.org/apps/target-tool/api/v1/targets/export/?api_key={api_key}&format=json"
    
    print(f"📡 Harvesting via Export API...")
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            
            data_dir = project_root / "data"
            data_dir.mkdir(exist_ok=True)
            
            with open(data_dir / "targets.json", "w") as f:
                json.dump(data, f, indent=4)
            print(f"✅ Success! Harvested {len(data)} targets into the library.")
        else:
            print(f"❌ Failed: {response.status_code}")
            # Dorknoper style debugging
            if response.status_code == 404:
                print("Hint: The API endpoint might have changed its routing again.")
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    harvest()
