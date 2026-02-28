#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Objective: Infrared sky-clarity monitor using MLX90614 to prevent imaging in fog.
"""
"""
Filename: core/preflight/fog_monitor.py
Version: 1.0.0 (Kwetal)
Role: Safety Gate - Clarity Provider
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
        delta = self.sensor.ambient_temperature - self.sensor.object_temperature
        return delta > self.threshold
        
fog_monitor = FogMonitor()
