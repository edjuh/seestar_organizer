import os
import time
import shutil
import requests
from pathlib import Path

# --- VERIFIED CONFIG FOR USER ED ---
SEESTAR_IP = "192.168.178.55"
ALP_API = f"http://{SEESTAR_IP}:5555/api/state"
SMB_SOURCE = Path("/mnt/seestar/MyWorks")
NAS_PARKING = Path("/mnt/astronas/parking_lot")

def check_mounts():
    if not os.path.ismount("/mnt/seestar"):
        print("❌ [Harvester] Seestar SMB not mounted!", flush=True)
        return False
    if not os.path.ismount("/mnt/astronas"):
        print("❌ [Harvester] NAS not mounted!", flush=True)
        return False
    return True

if __name__ == "__main__":
    print("📡 [Harvester] Booting up...", flush=True)
    
    if not check_mounts():
        time.sleep(10) # Wait before systemd restarts
        os._exit(1)

    print(f"✅ [Harvester] Watching {SEESTAR_IP} -> {NAS_PARKING}", flush=True)
    
    while True:
        try:
            # For now, we do a "Blind Sweep" of any .fits found in SMB_SOURCE
            # to verify the physical move works before adding API logic.
            for fits in SMB_SOURCE.rglob("*.fits"):
                dest = NAS_PARKING / "incoming_vibration"
                dest.mkdir(exist_ok=True)
                
                print(f"🚚 [Harvester] Moving {fits.name}...", flush=True)
                shutil.move(str(fits), str(dest / fits.name))
                print(f"✅ [Harvester] Moved to {dest}", flush=True)
                
            time.sleep(10)
        except Exception as e:
            print(f"⚠️ [Harvester] Error during sweep: {e}", flush=True)
            time.sleep(10)
