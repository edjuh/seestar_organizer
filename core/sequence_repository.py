import json
from pathlib import Path
import time

class SequenceRepository:
    def __init__(self):
        # Point to the persistent data folder
        self.data_dir = Path(__file__).parent.parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.targets_file = self.data_dir / "campaign_targets.json"

    def save_targets(self, targets_list):
        """Saves the normalized target list to disk with metadata."""
        payload = {
            "meta": {
                "fetched_utc": time.time(),
                "count": len(targets_list),
                "source": "AAVSO TargetTool"
            },
            "targets": targets_list
        }
        
        with open(self.targets_file, "w") as f:
            json.dump(payload, f, indent=2)
            
        print(f"✅ Saved {len(targets_list)} targets to {self.targets_file.name}")

    def load_targets(self):
        """Loads the targets from disk. Returns empty list if missing."""
        if self.targets_file.exists():
            with open(self.targets_file, "r") as f:
                data = json.load(f)
                return data.get("targets", [])
        return []
