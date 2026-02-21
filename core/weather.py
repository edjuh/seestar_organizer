"""
Filename: core/weather.py
Purpose: The Weather Gatekeeper. Uses consensus between Meteoblue 
         and 7Timer to ensure research-grade sky conditions.
"""
import requests
import json
import sys
import argparse

# SIKBOCK Thresholds for AAVSO Photometry
STRICT_PICTO_LIMIT = 2 # 1=Clear, 2=Mostly Clear
MAX_CLOUD_SCORE = 3    # 7Timer: 1-9 scale (3 is ~30% cover)
MAX_SEEING_SCORE = 6   # 7Timer: 1-8 scale (Lower is more stable)

class WeatherGate:
    def __init__(self, lat=52.3874, lon=4.6462, api_key="SCVxG4meyYvdUENk"):
        self.lat = lat
        self.lon = lon
        self.api_key = api_key

    def get_meteoblue(self):
        """Fetches general conditions and precipitation."""
        url = f"https://my.meteoblue.com/packages/basic-1h_basic-day?lat={self.lat}&lon={self.lon}&apikey={self.api_key}&format=json"
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            current_pic = data['data_1h']['pictocode'][0]
            precip = data['data_1h']['precipitation'][0]
            return {"pictocode": current_pic, "precip": precip}
        except:
            return None

    def get_7timer(self):
        """Fetches astronomical seeing and transparency."""
        url = f"https://www.7timer.info/bin/astro.php?lon={self.lon}&lat={self.lat}&ac=0&unit=metric&output=json"
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            current = data['dataseries'][0]
            return {
                "clouds": current['cloudcover'],
                "seeing": current['seeing'],
                "transparency": current['transparency']
            }
        except:
            return None

    def check_safety(self, simulate=False):
        """Returns (bool_is_safe, message) based on consensus."""
        if simulate:
            return True, "✨ SIMULATION: Skies are perfectly clear (Professor Sikbock approved)."

        mb = self.get_meteoblue()
        st = self.get_7timer()

        if not mb or not st:
            return False, "⚠️ SENSOR ERROR: Weather APIs unreachable. Safety first: ABORT."

        # 1. Check for Rain/Snow/Fog (Immediate Danger)
        if mb['precip'] > 0:
            return False, f"❌ DANGER: Precipitation detected ({mb['precip']}mm)."

        # 2. Check general cloudiness (Meteoblue)
        if mb['pictocode'] > STRICT_PICTO_LIMIT:
            return False, f"❌ CLOUDY: Meteoblue Condition {mb['pictocode']} is unsuitable."

        # 3. Check specific cloud cover (7Timer)
        if st['clouds'] > MAX_CLOUD_SCORE:
            return False, f"❌ CLOUDY: 7Timer Cloud Score {st['clouds']}/9 is too high."

        # 4. Check Atmospheric Stability (Seeing)
        if st['seeing'] > MAX_SEEING_SCORE:
            return False, f"❌ POOR SEEING: Atmosphere too unstable ({st['seeing']}/8)."

        return True, "✅ CLEAR SKIES: Consensus reached. Go for photons."

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="S30-PRO Weather Gatekeeper")
    parser.add_argument("--simulate", action="store_true", help="Force a 'Safe' result for testing.")
    args = parser.parse_args()

    # Load from environment or config in production; here we use defaults for now
    gate = WeatherGate()
    is_safe, msg = gate.check_safety(simulate=args.simulate)
    
    print("-" * 50)
    print(f"--- 🔭 Weather Gate v2.0 ---")
    print(msg)
    print("-" * 50)
    
    # Exit code allows shell scripts to use: ./weather.py && start_telescope
    sys.exit(0 if is_safe else 1)
