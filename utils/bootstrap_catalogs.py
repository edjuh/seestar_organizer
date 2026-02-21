"""
Filename: utils/bootstrap_catalogs.py
Role: One-time setup to populate the new tiered JSON structure.
"""
import json
from pathlib import Path

def bootstrap():
    data_dir = Path("data")
    
    # 1. Populate Priority (Moving your verified anchors here)
    priority_targets = [
        {"name": "SS Cyg", "ra": 325.68, "dec": 43.58, "mag": "8.2", "type": "UGSS", "priority": 1, "sector": "Cyg"},
        {"name": "U Gem", "ra": 119.33, "dec": 21.95, "mag": "8.2", "type": "UGSS", "priority": 1, "sector": "Gem"},
        {"name": "RX And", "ra": 1.15, "dec": 41.17, "mag": "10.3", "type": "UGZ", "priority": 1, "sector": "And"},
        {"name": "TT Ari", "ra": 31.72, "dec": 15.29, "mag": "10.5", "type": "VY", "priority": 1, "sector": "Ari"}
    ]
    with open(data_dir / "priority.json", "w") as f:
        json.dump({"targets": priority_targets}, f, indent=4)

    # 2. Populate Easy (The AAVSO 'Easy Stars' we discussed)
    easy_targets = [
        {"name": "Betelgeuse", "ra": 88.79, "dec": 7.41, "mag": "0.5", "type": "SRc", "sector": "Ori"},
        {"name": "Algol", "ra": 46.10, "dec": 40.95, "mag": "2.1", "type": "EA", "sector": "Per"},
        {"name": "Mira", "ra": 34.84, "dec": -2.98, "mag": "2.0", "type": "M", "sector": "Cet"},
        {"name": "Delta Cep", "ra": 337.29, "dec": 58.41, "mag": "3.5", "type": "DCEP", "sector": "Cep"}
    ]
    with open(data_dir / "easy.json", "w") as f:
        json.dump({"targets": easy_targets}, f, indent=4)

    # 3. Populate User (Just a placeholder for now)
    user_targets = [
        {"name": "M42", "ra": 83.82, "dec": -5.39, "mag": "4.0", "type": "Nebula", "sector": "Ori"}
    ]
    with open(data_dir / "user.json", "w") as f:
        json.dump({"targets": user_targets}, f, indent=4)

    print("[*] LCARS Database Synchronized.")
    print("[*] Files Updated: priority.json, easy.json, user.json")

if __name__ == "__main__":
    bootstrap()
