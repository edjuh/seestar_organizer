"""
Filename: tests/test_sensors.py
Objective: Verify I2C communication with the MLX90614 IR sensor.
Usage: python3 tests/test_sensors.py
Note: Checks if the Fog Monitor hardware is physically responsive.
"""
try:
    from core.fog_monitor import fog_monitor
    print(f"🔍 Ambient: {fog_monitor.sensor.ambient_temperature:.2f}C")
    print(f"🔍 Object:  {fog_monitor.sensor.object_temperature:.2f}C")
    print("✅ IR Sensor responding on I2C bus.")
except Exception as e:
    print(f"❌ Sensor Test Failed: {e}")
