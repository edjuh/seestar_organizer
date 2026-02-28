"""
Objective: System-wide logging with automatic file rotation.
"""
"""
Filename: core/logger.py
Usage: from core.logger import log_event; log_event("Slew complete")
Note: Retains 3 backup files of 5MB each.
"""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "seestar_joost.log"

handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger("S30-PRO")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def log_event(message, level="info"):
    if level == "error":
        logger.error(message)
    else:
        logger.info(message)
