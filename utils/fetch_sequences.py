import time
import json
from pathlib import Path
import sys

# Ensure Python can find 'core'
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from core.aavso_client import AAVSOClient
from core.sequence_repository import SequenceRepository

def run_scraper():
    print("🐌 Starting S30-PRO Polite Sequence Scraper...")
    client = AAVSOClient()
    repo = SequenceRepository()
    
    seq_dir = repo.data_dir / "sequences"
    seq_dir.mkdir(exist_ok=True)
    
    targets = repo.load_targets()
    if not targets:
        print("❌ No targets found. Run python3 -m utils.sync_catalog first.")
        return
        
    # Filter for S30-PRO Sweet Spot
    valid_types = ("M", "SR", "ZAND", "CEP", "DCEP")
    s30_targets = []
    for t in targets:
        vt = t.get("var_type", "").upper()
        # Handle complex types like 'ZAND+SR' or 'M:'
        parts = vt.replace(":", " ").replace("+", " ").split()
        if any(p in valid_types for p in parts) or any(p.startswith("SR") for p in parts):
            s30_targets.append(t)
            
    print(f"🎯 Filtered {len(targets)} raw targets down to {len(s30_targets)} S30-PRO candidates.")
    
    for idx, target in enumerate(s30_targets):
        star = target.get("star_name")
        safe_name = star.replace(" ", "_").lower()
        file_path = seq_dir / f"{safe_name}.json"
        
        if file_path.exists():
            print(f"⏭️  [{idx+1}/{len(s30_targets)}] Skipping {star} (Already cached)")
            continue
            
        print(f"🛰️  [{idx+1}/{len(s30_targets)}] Fetching V-band sequence for {star} ({target.get('var_type')})...")
        sequence = client.fetch_sequence(star)
        
        if sequence:
            with open(file_path, "w") as f:
                json.dump(sequence, f, indent=2)
            print(f"  ✅ Saved {len(sequence)} comparison stars.")
            
            # The Sysadmin Signature
            if idx < len(s30_targets) - 1:
                print("  💤 Sleeping for 3.14 minutes (188.4s) to respect AAVSO servers...")
                time.sleep(188.4)
        else:
            print(f"  ⚠️  No valid V-band sequence found for {star}.")
            time.sleep(10) # Short backoff on failure

if __name__ == "__main__":
    run_scraper()
