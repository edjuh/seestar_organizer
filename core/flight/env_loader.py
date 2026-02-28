"""
Objective: Centralized configuration and environment variable manager.
"""
"""
Filename: core/env_loader.py
Usage: from core.env_loader import cfg
Note: Ensures AAVSO_TARGET_KEY and other secrets are present at runtime.
"""
import os
import tomllib
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / ".env")

def cfg(key, default=None):
    """Retrieves a setting from environment or config.toml."""
    val = os.getenv(key)
    if val: return val
    
    # Fallback to config.toml
    config_path = PROJECT_ROOT / "config.toml"
    if config_path.exists():
        with open(config_path, "rb") as f:
            data = tomllib.load(f)
            # Simple flat search for now
            return data.get(key, default)
    return default
