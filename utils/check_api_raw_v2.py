import requests
import os
import socket

def get_env_key(key_name):
    if not os.path.exists(".env"): return None
    with open(".env", "r") as f:
        for line in f:
            if line.startswith(key_name):
                return line.strip().split("=")[1].strip('"')

def check_gps_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect(("localhost", 2947))
        print("✅ GPSD: Socket 2947 is OPEN")
    except Exception as e:
        print(f"❌ GPSD: Errno 111 - Is the service running? ({e})")

def check_weather_pipeline():
    # 1. Open-Meteo (No Key) - Reliable Fallback
    om_url = "https://api.open-meteo.com/v1/forecast?latitude=52.38&longitude=4.64&current=cloud_cover,surface_pressure&hourly=visibility"
    r_om = requests.get(om_url)
    print(f"{'✅' if r_om.status_code == 200 else '❌'} Open-Meteo Status: {r_om.status_code}")
    
    # 2. Meteoblue (Seeing Data)
    mb_key = get_env_key("METEOBLUE_KEY")
    mb_url = f"https://my.meteoblue.com/packages/astronomy?lat=52.38&lon=4.64&apikey={mb_key}&format=json"
    r_mb = requests.get(mb_url)
    print(f"{'✅' if r_mb.status_code == 200 else '❌'} Meteoblue Status: {r_mb.status_code} (Text: {r_mb.text[:50]})")

def check_aavso_auth():
    # Using the TargetTool token to verify we can talk to the database
    key = get_env_key("AAVSO_TARGET_KEY")
    url = "https://targettool.aavso.org/TargetTool/api/v1/targets"
    headers = {"Authorization": f"Token {key}"}
    r = requests.get(url, headers=headers)
    print(f"{'✅' if r.status_code == 200 else '❌'} AAVSO Auth Status: {r.status_code}")

if __name__ == "__main__":
    print("--- Discovery Test v2 ---")
    check_gps_socket()
    check_weather_pipeline()
    check_aavso_auth()
