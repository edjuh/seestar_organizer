"""
Filename: utils/defrag_monitor.py
Objective: Visual Defragmenter with ETA and Last-Star-Fetched ticker.
Usage: python3 -m utils.defrag_monitor
"""
import json
import time
import os
from pathlib import Path
from datetime import timedelta

def get_status():
    root = Path(__file__).parent.parent
    targets_file = root / "data" / "targets.json"
    seq_dir = root / "data" / "sequences"
    
    if not targets_file.exists(): return None

    with open(targets_file, 'r') as f:
        targets = json.load(f)

    cached_paths = list(seq_dir.glob("*.json"))
    cached_names = {f.stem for f in cached_paths}
    
    # Map the grid
    grid = []
    for t in targets:
        name = t['star_name'].replace(" ", "_").lower()
        grid.append("■" if name in cached_names else ".")
    
    # Identify last file written to disk
    last_star = "Waiting..."
    if cached_paths:
        last_file = max(cached_paths, key=lambda p: p.stat().st_mtime)
        last_star = last_file.stem.replace("_", " ").title()
        
    return grid, len(targets), len(cached_names), last_star

def run():
    PI_SLEEP = 188.4
    try:
        while True:
            data = get_status()
            if not data:
                print("Waiting for data...")
                time.sleep(5)
                continue
            
            grid, total, have, last_star = data
            missing = total - have
            eta_seconds = missing * PI_SLEEP
            eta_str = str(timedelta(seconds=int(eta_seconds)))

            os.system('clear')
            print(f"🔭 S30-PRO VAULT DEFRAGMENTER | {have}/{total} Cached")
            print("-" * 50)
            
            # Print grid in rows of 25
            for i in range(0, len(grid), 25):
                print(" ".join(grid[i:i+25]))
            
            print("-" * 50)
            print(f"Progress:    {(have/total)*100:.1f}%")
            print(f"Last In:     {last_star}")
            print(f"Est. Finish: {eta_str}")
            print(f"Status:      Watching the drip...")
            print("\n(Press Ctrl+C to exit monitor)")
            time.sleep(30)
    except KeyboardInterrupt:
        print("\nMonitor closed. Back to the Academy!")

if __name__ == "__main__":
    run()
