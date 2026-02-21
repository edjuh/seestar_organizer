import time
from core.gps import gps_station
from core.weather import weather_station

def test_snapshot():
    print("Starting... waiting 3 seconds for background threads to fetch initial data...")
    time.sleep(3)
    
    gps_data = gps_station.get_state()
    weather_data = weather_station.get_state()
    
    print("\n--- 🛰️  GPS Snapshot ---")
    for k, v in gps_data.items():
        print(f"  {k}: {v}")
        
    print("\n--- 🌤️  Weather Snapshot ---")
    for k, v in weather_data.items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    test_snapshot()
