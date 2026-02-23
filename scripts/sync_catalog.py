"""
Filename: scripts/sync_catalog.py
Objective: Sync the local target library with current AAVSO Alert Notice targets.
Usage: python3 -m scripts.sync_catalog
Note: This is the data-source for the Nightly Planner.
"""
import json
from pathlib import Path
from core.aavso_client import AAVSOClient

def sync():
    client = AAVSOClient()
    print("🛰️ Synchronizing AAVSO Target Library...")
    targets = client.fetch_campaign_targets()
    
    if targets:
        path = Path(__file__).parent.parent / "data" / "targets.json"
        path.parent.mkdir(exist_ok=True)
        with open(path, "w") as f:
            json.dump(targets, f, indent=4)
        print(f"✅ Library Updated: {len(targets)} targets.")
    else:
        print("❌ Sync failed. Verify .env AAVSO_TARGET_KEY.")

if __name__ == "__main__":
    sync()
