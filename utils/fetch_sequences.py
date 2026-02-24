"""
Filename: utils/fetch_sequences.py
Objective: Downloads specific V-band comparison sequences for identified targets.
"""
"""
Filename: utils/fetch_sequences.py
Version: 1.3.1
Objective: Systematic authenticated harvest with automatic manifest verification and deduplication.
"""
import time
import json
import shutil
from pathlib import Path
from core.aavso_client import client
from core.sequence_repository import repo
from utils.verify_library import verify

# Clear local cache on startup
for p in Path('.').rglob('__pycache__'):
    shutil.rmtree(p, ignore_errors=True)

def run_scraper():
    raw_targets = repo.load_targets()
    
    # Deduplicate and clean star names
    unique_stars = set()
    targets = []
    for t in raw_targets:
        star = " ".join(t.get("star_name", "").split())
        if star and star not in unique_stars:
            unique_stars.add(star)
            t["star_name"] = star # Update dictionary with clean name
            targets.append(t)
            
    # Sort alphabetically for a predictable run
    targets = sorted(targets, key=lambda x: x["star_name"])
    
    print(f"🐌 Librarian starting harvest for {len(targets)} unique stars...")
    
    for idx, target in enumerate(targets):
        star = target.get("star_name")
        
        safe_name = star.replace(" ", "_").lower() + ".json"
        if (repo.seq_dir / safe_name).exists():
            continue
            
        print(f"🛰️ [{idx+1}/{len(targets)}] Requesting {star}...")
        seq = client.fetch_sequence(star)
        
        if seq:
            with open(repo.seq_dir / safe_name, 'w') as f:
                json.dump(seq, f, indent=2)
            
            print(f"  ✅ Saved {len(seq)} comparison stars. Updating Verified Manifest...")
            verify() 
            
            print(f"  💤 Initiating Pi-Sleep (188.4s)...")
            time.sleep(188.4) # Fixed the decimal to strictly enforce the 3.14 minute limit
        else:
            print(f"  ❌ No data/Error for {star}. Moving on...")
            time.sleep(10)

if __name__ == "__main__":
    run_scraper()
