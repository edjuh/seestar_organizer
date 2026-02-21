import requests
import os

def get_env_key(key_name):
    if not os.path.exists(".env"): return None
    with open(".env", "r") as f:
        for line in f:
            if line.startswith(key_name):
                return line.strip().split("=")[1].strip('"')

def check_weather():
    key = get_env_key("METEOBLUE_KEY")
    url = f"https://my.meteoblue.com/packages/astronomy-basic?lat=52.38&lon=4.64&apikey={key}"
    r = requests.get(url)
    print(f"{'✅' if r.status_code == 200 else '❌'} Meteoblue Status: {r.status_code}")

def check_aavso():
    key = get_env_key("AAVSO_TARGET_KEY")
    # Testing the TargetTool API for REDA campaign
    url = f"https://targettool.aavso.org/api/v1/targets/?target_list=REDA"
    headers = {"Authorization": f"Token {key}"}
    r = requests.get(url, headers=headers)
    print(f"{'✅' if r.status_code == 200 else '❌'} AAVSO REDA Status: {r.status_code}")
    if r.status_code == 200:
        print(f"   Targets found: {len(r.json())}")

if __name__ == "__main__":
    check_weather()
    check_aavso()
