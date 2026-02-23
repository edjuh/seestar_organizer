"""
Filename: utils/check_progress.py
Version: 1.1.0
Objective: Track harvest progress and identify the most recent acquisition.
"""
import json
from pathlib import Path

def check():
    root = Path(__file__).parent.parent
    targets_file = root / "data" / "targets.json"
    seq_dir = root / "data" / "sequences"
    
    if not targets_file.exists():
        print("❌ targets.json not found.")
        return

    with open(targets_file, 'r') as f:
        targets = json.load(f)

    target_names = {t['star_name'].replace(" ", "_").lower() for t in targets}
    cached_paths = list(seq_dir.glob("*.json"))
    cached_names = {f.stem for f in cached_paths}
    
    total = len(target_names)
    have = len(cached_names.intersection(target_names))
    missing = total - have
    percent = (have / total) * 100 if total > 0 else 0

    # Identify last star fetched by file modification time
    if cached_paths:
        last_file = max(cached_paths, key=lambda p: p.stat().st_mtime)
        last_star = last_file.stem.replace("_", " ").title()
    else:
        last_star = "None"

    print("="*40)
    print("🔭 HARVEST PROGRESS REPORT")
    print("="*40)
    print(f"Total Targets:    {total}")
    print(f"Cached Sequences: {have}")
    print(f"Completion:       {percent:.1f}%")
    print(f"Last Star:        {last_star}")
    print("="*40)

if __name__ == "__main__":
    check()
