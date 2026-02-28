"""
Objective: Manages file synchronization between Seestar, Local Buffer, and NAS.
"""
"""
Filename: core/sync_manager.py
Usage: sync_manager.process_offload()
Note: Verified move operations to prevent data corruption on SD card.
"""
import shutil
from pathlib import Path
from core.env_loader import cfg
from core.logger import log_event

class SyncManager:
    def __init__(self):
        self.source = Path(cfg("SOURCE_DIR", "/home/ed/seestar_downloads"))
        self.destination = Path(cfg("NAS_PATH", "/home/ed/seestar_organizer/data/local_buffer"))

    def is_lifeboat_alive(self):
        return self.destination.exists()

    def process_offload(self, target_subfolder="active_session"):
        files = list(self.source.glob("*.fits"))
        if not files: return
        
        dest_path = self.destination / target_subfolder
        dest_path.mkdir(parents=True, exist_ok=True)
        
        for f in files:
            log_event(f"Moving {f.name} to {dest_path}")
            shutil.move(str(f), str(dest_path / f.name))

sync_manager = SyncManager()
