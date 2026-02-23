import os
import time
from pathlib import Path

# Paths verified by user ed
NAS_DIR = Path("/mnt/astronas/parking_lot")
SSD_DIR = Path("/home/ed/seestar_organizer/data/local_buffer")

def test_path(path_obj, label):
    print(f"🔍 Checking {label}: {path_obj}...", flush=True)
    try:
        path_obj.mkdir(parents=True, exist_ok=True)
        test_file = path_obj / f".vibe_check_{label}"
        
        # 1. Touch (Create)
        test_file.touch()
        # 2. Verify (Exists)
        if test_file.exists():
            # 3. Unlink (Remove)
            test_file.unlink()
            print(f"✅ {label} [OK]: Write/Verify/Delete sequence passed.", flush=True)
            return True
        else:
            print(f"❌ {label} [FAIL]: File touch reported success but file missing.", flush=True)
            return False
    except Exception as e:
        print(f"❌ {label} [CRITICAL]: {e}", flush=True)
        return False

if __name__ == "__main__":
    print("--- DUAL-STORAGE PULSE CHECK ---", flush=True)
    
    nas_ok = test_path(NAS_DIR, "NAS_CIFS")
    ssd_ok = test_path(SSD_DIR, "LOCAL_SSD")
    
    if nas_ok and ssd_ok:
        print("🚀 INFRASTRUCTURE READY: Primary and Fallback paths verified.", flush=True)
    else:
        print("⚠️ INFRASTRUCTURE WEAK: One or more paths failed.", flush=True)
    
    # Stay alive for service log capture
    while True:
        time.sleep(60)
