import tomllib
import os
from pathlib import Path

class Config:
    _data = {}
    _secrets = {}
    _loaded = False

    @classmethod
    def load(cls):
        if cls._loaded:
            return
            
        base_path = Path(__file__).parent.parent
        
        # 1. Load System Settings (TOML)
        toml_path = base_path / "config.toml"
        if toml_path.exists():
            with open(toml_path, "rb") as f:
                cls._data = tomllib.load(f)
        else:
            print("WARNING: config.toml not found!")

        # 2. Load Secrets (.env) safely
        env_path = base_path / ".env"
        if env_path.exists():
            with open(env_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if "=" in line and not line.startswith("#"):
                        key, val = line.split("=", 1)
                        cls._secrets[key.strip()] = val.strip().strip('"').strip("'")
        
        cls._loaded = True

    @classmethod
    def get(cls, section, key=None, default=None):
        if not cls._loaded:
            cls.load()
            
        # If no specific key is asked, they might be asking for a root-level secret
        if key is None:
            return cls._secrets.get(section, default)
            
        # Otherwise, fetch from the TOML dictionary structure
        return cls._data.get(section, {}).get(key, default)

# Global helper function for clean imports in other files
def cfg(section, key=None, default=None):
    return Config.get(section, key, default)

# Pre-load on import
Config.load()
