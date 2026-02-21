"""
Filename: core/env_loader.py
Version: 0.7.0
Role: Securely loads observer credentials from .env
Owner: Ed de la Rie (PE5ED)
"""
import os
from pathlib import Path

def get_observer_info():
    """
    Reads AAVSO_CODE and OBSERVER_NAME from .env.
    Uses robust split logic to avoid ValueErrors on malformed lines.
    """
    env_path = Path(".env")
    info = {"code": "GUEST", "name": "Anonymous Observer"}
    
    if not env_path.exists():
        return info

    try:
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                
                parts = line.split("=", 1)
                if len(parts) == 2:
                    key, val = parts
                    val = val.strip().replace('"', '').replace("'", "")
                    if key == "AAVSO_CODE": 
                        info["code"] = val
                    elif key == "OBSERVER_NAME": 
                        info["name"] = val
    except Exception:
        pass # Fallback to defaults
        
    return info
