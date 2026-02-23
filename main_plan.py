"""
Filename: main_plan.py
Objective: Generate a nightly schedule from verified photometry targets.
Usage: python3 main_plan.py
"""
import json
from pathlib import Path
from core.nightly_planner import NightlyPlanner
from core.logger import log_event

def main():
    root = Path(__file__).parent
    verified_file = root / "data" / "observable_targets.json"
    
    if not verified_file.exists():
        print("❌ Error: No observable_targets.json found.")
        print("💡 Run 'python3 -m utils.verify_library' first.")
        return

    print("🔭 S30-PRO: Loading Verified Manifest...")
    with open(verified_file, 'r') as f:
        targets = json.load(f)
        
    print(f"✅ Found {len(targets)} stars with valid photometry sequences.")
    
    # Initialize the Planner (Alexander Pieps) with verified data
    planner = NightlyPlanner(manifest=targets)
    plan = planner.generate_manifest()
    
    if plan:
        print(f"🚀 Nightly Plan generated: {len(plan)} targets scheduled.")
    else:
        print("⚠️ No verified targets are currently observable in the sky.")

if __name__ == "__main__":
    main()
