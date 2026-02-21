"""
Filename: utils/expand_catalogs.py
Version: 0.8.7
Role: Populate the Tiered JSON files with a wider array of targets.
"""
import json
from pathlib import Path

def expand():
    data_dir = Path("data")
    
    # --- EASY CATALOG (Bright, High Amplitude) ---
    easy_stars = [
        {"name": "Betelgeuse", "ra": 88.79, "dec": 7.41, "mag": "0.5", "type": "SRc", "sector": "Ori"},
        {"name": "Algol", "ra": 46.10, "dec": 40.95, "mag": "2.1", "type": "EA", "sector": "Per"},
        {"name": "Mira", "ra": 34.84, "dec": -2.98, "mag": "2.0", "type": "M", "sector": "Cet"},
        {"name": "Delta Cep", "ra": 337.29, "dec": 58.41, "mag": "3.5", "type": "DCEP", "sector": "Cep"},
        {"name": "Eta Aql", "ra": 296.88, "dec": 0.97, "mag": "3.5", "type": "DCEP", "sector": "Aql"},
        {"name": "R Leo", "ra": 146.87, "dec": 11.43, "mag": "4.4", "type": "M", "sector": "Leo"},
        {"name": "Chi Cyg", "ra": 297.70, "dec": 32.91, "mag": "3.3", "type": "M", "sector": "Cyg"},
        {"name": "W Ori", "ra": 76.35, "dec": 1.18, "mag": "5.9", "type": "SRb", "sector": "Ori"},
        {"name": "R Sct", "ra": 281.88, "dec": -5.71, "mag": "4.2", "type": "RVA", "sector": "Sct"}
    ]
    
    # --- FULL CATALOG (The broader Variable Sweep) ---
    full_sweep = [
        {"name": "V CVn", "ra": 199.14, "dec": 45.52, "mag": "6.5", "type": "SRa", "sector": "CVn"},
        {"name": "RT Cyg", "ra": 295.84, "dec": 48.78, "mag": "6.0", "type": "M", "sector": "Cyg"},
        {"name": "T Cep", "ra": 317.32, "dec": 68.49, "mag": "5.2", "type": "M", "sector": "Cep"},
        {"name": "S Vir", "ra": 200.75, "dec": -7.18, "mag": "6.3", "type": "M", "sector": "Vir"},
        {"name": "RR Lyr", "ra": 285.42, "dec": 42.78, "mag": "7.1", "type": "RRAB", "sector": "Lyr"},
        {"name": "U Mon", "ra": 112.72, "dec": -9.78, "mag": "5.9", "type": "RVB", "sector": "Mon"}
    ]

    # Writing to files
    with open(data_dir / "easy.json", "w") as f:
        json.dump({"targets": easy_stars}, f, indent=4)
        
    with open(data_dir / "full.json", "w") as f:
        json.dump({"targets": full_sweep}, f, indent=4)

    print(f"[*] Data Sideload Complete: {len(easy_stars)} Easy, {len(full_sweep)} Full.")

if __name__ == "__main__":
    expand()
