"""
Filename: core/fog_monitor.py
Objective: Infrared sky-clarity monitor using MLX90614.
Usage: if fog_monitor.is_sky_clear(): ...
Note: A small Delta indicates clouds/fog; a large Delta indicates clear sky.
"""
import board
import busio
import adafruit_mlx90614

class FogMonitor:
    def __init__(self, threshold=10):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_mlx90614.MLX90614(self.i2c)
        self.threshold = threshold

    def is_sky_clear(self):
        # Delta = Ambient Temp - Sky (Object) Temp
        delta = self.sensor.ambient_temperature - self.sensor.object_temperature
        return delta > self.threshold
        
fog_monitor = FogMonitor()
