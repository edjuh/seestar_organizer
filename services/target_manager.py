"""
Filename: services/target_manager.py
Version: 0.9.8
"""
import time, json, os, sys
import tomllib
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.target_manager import TargetManager
from utils.weather_safety import WeatherSafety

def run_service():
    with open(PROJECT_ROOT / "config.toml", "rb") as f:
        config = tomllib.load(f)
    
    manager = TargetManager(config)
    weather = WeatherSafety(lat=config.get('latitude', 52.38), lon=config.get('longitude', 4.64))
    LOG_DIR = PROJECT_ROOT / "logs"

    while True:
        try:
            w_status = weather.check()
            now = datetime.now(timezone.utc)
            
            for cat in ["priority", "easy", "user", "full"]:
                results = manager.process_catalog(cat)
                
                # Ensuring last_sync is a string
                last_update = str(results.get("last_update", now.isoformat()))

                payload = {
                    "observable": results["observable"],
                    "weather": w_status,
                    "daemon_health": {
                        "status": "NOMINAL" if w_status['safe'] else "STANDBY",
                        "last_sync": last_update,
                        "safe": w_status['safe']
                    }
                }
                
                final_path = LOG_DIR / f"status_{cat}.json"
                tmp_path = final_path.with_suffix(".tmp")
                with open(tmp_path, "w") as f:
                    json.dump(payload, f, indent=4)
                os.replace(tmp_path, final_path)

            print(f"[HB] {now.strftime('%H:%M:%S')} | Predictor Sync Success.")
        except Exception as e:
            print(f"[ERR] Orchestrator Failure: {e}")
            
        time.sleep(30)

if __name__ == "__main__":
    run_service()
