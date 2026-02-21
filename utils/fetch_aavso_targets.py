"""
Filename: utils/fetch_aavso_targets.py
Version: 0.7.5.5 (Open Pipe Mode)
"""
import requests
import json
import time
from pathlib import Path

def fetch():
    anchors = ["SS Cyg", "Z Cam", "U Gem", "T CrB", "V Sge", "AM Her", "SU UMa", "RX And", "TT Ari"]
    all_targets = []
    seen_oids = set()
    
    print(f"[*] LCARS LONG-RANGE SCAN: OPEN PIPE MODE")

    for name in anchors:
        ident = name.replace(" ", "+")
        # Step 1: Get Anchor for its coordinates and constellation
        url = f"https://vsx.aavso.org/index.php?view=api.object&ident={ident}&format=json"
        try:
            r = requests.get(url, timeout=10)
            obj_data = r.json().get("VSXObject")
            if isinstance(obj_data, list): obj_data = obj_data[0]
            if not obj_data: continue

            ra = obj_data.get("RA2000")
            dec = obj_data.get("Declination2000")
            const = obj_data.get("Constellation", "Unknown")

            # Step 2: Pull the entire neighborhood list (Radius 2.0)
            # We remove the 'tomag' filter to ensure we get a response
            search_url = f"https://vsx.aavso.org/index.php?view=api.list&ra={ra}&dec={dec}&radius=2.0&format=json"
            sr = requests.get(search_url, timeout=10)
            
            raw_list = sr.json().get("VSXObjects")
            
            # Normalize to list
            neighbors = []
            if isinstance(raw_list, list):
                neighbors = raw_list
            elif isinstance(raw_list, dict):
                neighbors = [raw_list]
            
            # If radius search is empty, manually add the anchor
            if not neighbors:
                neighbors = [obj_data]

            for n in neighbors:
                oid = n.get("OID")
                if oid and oid not in seen_oids:
                    all_targets.append({
                        "name": n.get("Name"),
                        "ra": n.get("RA2000"),
                        "dec": n.get("Declination2000"),
                        "mag": n.get("MaxMag", "??"),
                        "type": n.get("Type", "??"),
                        "priority": 1 if n.get("Name") == name else 2,
                        "sector": const
                    })
                    seen_oids.add(oid)
            
            print(f"[OK] Sector {const}: {len(neighbors)} objects identified.")
            time.sleep(1)
            
        except Exception as e:
            print(f"[!] Sensor Failure in Sector {name}: {e}")

    # Final Buffer Save
    if all_targets:
        Path("data").mkdir(exist_ok=True)
        with open("data/targets.json", "w") as f:
            json.dump({"targets": all_targets}, f, indent=4)
        print(f"\n[DONE] {len(all_targets)} targets cached in data/targets.json")
    else:
        print("[!] CRITICAL: No data retrieved from AAVSO.")

if __name__ == "__main__":
    fetch()
