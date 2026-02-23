"""
Filename: tests/test_joost.py
Objective: Core environment and dependency validation.
"""
import sys
from pathlib import Path

# --- THE GRIP: Path Anchor ---
# Adds the project root to the search path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.env_loader import cfg

def check_vitals():
    print(f"🐍 Python Version: {sys.version.split()[0]}")
    try:
        import dotenv
        print("✅ Library: python-dotenv is installed.")
    except ImportError:
        print("❌ Library: python-dotenv is MISSING. Run 'pip install python-dotenv'")
        return

    key = cfg("AAVSO_TARGET_KEY")
    if key and len(key) > 5:
        print("✅ Environment: .env loaded and key present.")
    else:
        print("❌ Environment: .env error or key missing.")

if __name__ == "__main__":
    check_vitals()
