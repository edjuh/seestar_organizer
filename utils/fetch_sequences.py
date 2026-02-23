"""
Filename: utils/fetch_sequences.py
Version: 1.3.0
Objective: Systematic authenticated harvest with automatic manifest verification.
"""
import time
import json
import os
import shutil
from pathlib import Path
from core.aavso_client import client
from core.sequence_repository import repo
from utils.verify_library import verify # The Kwetal Link

# Clear local cache on startup
for p in Path('.').rglob('__pycache__'):
    shutil.rmtree(p, ignore_errors=True)

def run_scraper():
    targets = repo.load_targets()
    print(f"🐌 Librarian starting harvest for {len(targets)} stars...")
    
    for idx, target in enumerate(targets):
        star = target.get("star_name")
        if repo.get_sequence(star):
            continue
            
        print(f"🛰️ [{idx+1}/{len(targets)}] Requesting {star}...")
        seq = client.fetch_sequence(star)
        
        if seq:
            safe_name = star.replace(" ", "_").lower() + ".json"
            with open(repo.seq_dir / safe_name, 'w') as f:
                json.dump(seq, f, indent=2)
            
            print(f"  ✅ Saved {len(seq)} stars. Updating Verified Manifest...")
            verify() # Automatically trigger the Quality Control filter
            
            print(f"  💤 Initiating Pi-Sleep (188.4s)...")
            time.sleep(188.4) 
        else:
            print(f"  ❌ No data/Error for {star}. Moving on...")
            time.sleep(10)

if __name__ == "__main__":
    run_scraper()
