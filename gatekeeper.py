import socket
import requests
import os
from core.env_loader import Config

def test_storage():
    paths = ["/mnt/data_ssd", "/mnt/astronas"]
    for p in paths:
        if os.path.ismount(p):
            print(f"✅ Mount: {p} is ACTIVE")
        else:
            print(f"❌ Mount: {p} is MISSING")

def test_gps_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect(("localhost", 2947))
        print("✅ GPSD: Socket 2947 is accepting connections")
    except Exception as e:
        print(f"❌ GPSD: Connection failed ({e})")

def test_weather_api():
    key = Config.get("METEOBLUE_KEY") # Fetching from .env via our loader
    url = f"https://my.meteoblue.com/packages/astronomy-basic?lat=52.38&lon=4.64&apikey={key}"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            print("✅ Meteoblue: API reachable and Key valid")
        else:
            print(f"❌ Meteoblue: Status {r.status_code}. Check your .env key.")
    except Exception as e:
        print(f"❌ Meteoblue: Request failed ({e})")

if __name__ == "__main__":
    print("--- Beunhaas v0.0 Gatekeeper ---")
    test_storage()
    test_gps_socket()
    test_weather_api()
