import requests

API_KEY = "SCVxG4meyYvdUENk"
LAT = "52.3874"
LON = "4.6462"
URL = f"https://my.meteoblue.com/packages/basic-1h?apikey={API_KEY}&lat={LAT}&lon={LON}&format=json"

def check_safety():
    try:
        r = requests.get(URL, timeout=10)
        if r.status_code == 200:
            data = r.json()['data_1h']
            pic = data['pictocode'][0]
            precip = data['precipitation'][0]
            
            # 1-4 is clear, 5 is partly cloudy. 
            # Anything above 5 usually means 50%+ cloud cover.
            weather_ok = pic <= 5 
            rain_ok = precip == 0
            
            print(f"--- Meteoblue Report ---")
            print(f"Pictocode (Condition): {pic}")
            print(f"Precipitation: {precip}mm")
            
            if weather_ok and rain_ok:
                print("\n✅ STATUS: CLEAR SKIES. GO FOR PHOTONS.")
                return True
            else:
                print("\n⚠️ STATUS: UNSAFE. CLOUDS OR RAIN DETECTED.")
                return False
        return False
    except Exception as e:
        print(f"Error checking weather: {e}")
        return False

if __name__ == "__main__":
    check_safety()
