"""
Background tasks: SafetyMonitor + Organizer.
Runs forever in daemon threads.
"""

from threading import Thread, Event
import time
from loguru import logger

from core.weather.monitor import safety_monitor
from core.organizer.archiver import archive_new_files
from core.config import settings

class OrganizerTask:
    def __init__(self):
        self.stop_event = Event()
        self.thread = None

    def start(self):
        if self.thread and self.thread.is_alive():
            return
        self.stop_event.clear()
        self.thread = Thread(target=self._run, daemon=True, name="OrganizerTask")
        self.thread.start()
        logger.info("Organizer background task started")

    def stop(self):
        self.stop_event.set()
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Organizer task stopped")

    def _run(self):
        while not self.stop_event.is_set():
            try:
                count = archive_new_files(dry_run=False)
                if count > 0:
                    logger.info(f"Organizer processed {count} new files")
            except Exception as e:
                logger.error(f"Organizer task error: {e}")
            time.sleep(settings.advanced.organizer_run_every_minutes * 60)

# Global
organizer_task = OrganizerTask()

def start_background_tasks():
    safety_monitor.start()
    organizer_task.start()
