import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from core.weather import weather

print("🌤️  Testing Ensemble Weather Monitor...")
print(f"📍 Location Loaded: Lat {weather.lat}, Lon {weather.lon}")
print(f"☁️  Cloud Threshold: {weather.max_clouds}%")
print("-" * 40)

is_safe = weather.is_safe_to_image()

print("-" * 40)
print(f"🚀 FINAL VERDICT: {'SAFE (True)' if is_safe else 'UNSAFE (False)'}")
