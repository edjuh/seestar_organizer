"""
Filename: core/validator.py
Objective: Enforce data integrity constraints for the S30-PRO pipeline.
"""
from pathlib import Path
import json
from core.logger import log_event

class SystemValidator:
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.manifest_path = self.root / "data" / "observable_targets.json"

    def is_plan_safe(self):
        """Checks if we have a verified manifest to plan from."""
        if not self.manifest_path.exists():
            log_event("Safety Check Failed: observable_targets.json missing.", level="error")
            return False
            
        with open(self.manifest_path, 'r') as f:
            targets = json.load(f)
            
        if not targets:
            log_event("Safety Check Failed: No verified targets available.", level="error")
            return False
            
        return True

    def validate_environment(self):
        """Ensure core directories exist."""
        dirs = ["data/sequences", "logs", "data/local_buffer"]
        for d in dirs:
            (self.root / d).mkdir(parents=True, exist_ok=True)
        return True

validator = SystemValidator()
