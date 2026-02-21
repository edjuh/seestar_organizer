#!/usr/bin/env python3
"""
Filename: utils/build_tonights_plan.py
Version: 0.7.1
Role: CLI Trigger to convert Target Manager JSON to Ekos XML.
Owner: Ed de la Rie (PE5ED)
"""
import json
import tomllib
import sys
import os
from pathlib import Path

# Fix: Ensure the project root is in sys.path regardless of where we call it from
project_root = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(project_root))

from core.ekos import EkosBridge

def main():
    config_path = project_root / "config.toml"
    status_path = project_root / "logs" / "target_status.json"
    
    # 1. Load Config
    if not config_path.exists():
        print(f"[!] Config missing at {config_path}")
        return
    with open(config_path, "rb") as f:
        config = tomllib.load(f)
    
    # 2. Load Target Data
    if not status_path.exists():
        print("[!] No target status found. Is the Target Manager service running?")
        return
    with open(status_path, "r") as f:
        data = json.load(f)
        targets = data.get("observable", [])

    if not targets:
        print("[!] Target list is empty. Waiting for Target Manager to score stars...")
        return

    # 3. Generate the .esl
    bridge = EkosBridge(config)
    output = bridge.generate_esl(targets)
    
    print(f"[OK] Generated Ekos Scheduler List: {output}")
    print(f"[*] Total Targets: {len(targets)}")

if __name__ == "__main__":
    main()
