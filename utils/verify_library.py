import json
from pathlib import Path
from core.logger import log_event

def verify():
    """Scans the JSON vault to ensure files are valid and not corrupted."""
    project_root = Path(__file__).parent.parent.resolve()
    seq_dir = project_root / "data" / "sequences"
    
    if not seq_dir.exists():
        log_event("VerifyLibrary: Sequences directory missing.")
        return False
        
    json_files = list(seq_dir.glob("*.json"))
    valid_count = 0
    corrupt_files = []
    
    for f in json_files:
        try:
            with open(f, 'r') as file:
                data = json.load(file)
                # Ensure it's a valid list with actual target data
                if isinstance(data, list) and len(data) > 0:
                    valid_count += 1
                else:
                    corrupt_files.append(f.name)
        except Exception:
            corrupt_files.append(f.name)
            
    log_event(f"VerifyLibrary: Scanned {len(json_files)} files. {valid_count} valid, {len(corrupt_files)} corrupt.")
    
    for cf in corrupt_files:
        log_event(f"VerifyLibrary: Corrupt file detected -> {cf}", level="warning")
        
    return len(corrupt_files) == 0

if __name__ == "__main__":
    verify()
