"""
Filename: core/gps.py
Version: 1.0.4
Purpose: Direct Serial GPS with Maidenhead Fallback.
"""
import threading
import serial
import time

class GPSMonitor(threading.Thread):
    def __init__(self, config: dict):
        super().__init__(daemon=True)
        # JO22hj21 fallback (Haarlem)
        self.data = {
            "lat": 52.3821, 
            "lon": 4.6015, 
            "alt": 0, 
            "status": "Grid Fallback (JO22hj)", 
            "fix": 0
        }
        self.port = "/dev/ttyUSB0" 
        self.running = True

    def run(self):
        while self.running:
            try:
                # Try 9600 first (standard for most USB GPS)
                with serial.Serial(self.port, 9600, timeout=1) as ser:
                    while self.running:
                        line = ser.readline().decode('ascii', errors='replace')
                        if '$GPGGA' in line:
                            self._parse_gga(line)
            except:
                time.sleep(10)

    def _parse_gga(self, line):
        parts = line.split(',')
        if len(parts) > 6 and parts[6] != '0':
            try:
                raw_lat = float(parts[2])
                lat = int(raw_lat/100) + (raw_lat%100)/60
                if parts[3] == 'S': lat = -lat
                
                raw_lon = float(parts[4])
                lon = int(raw_lon/100) + (raw_lon%100)/60
                if parts[5] == 'W': lon = -lon
                
                self.data.update({
                    "lat": round(lat, 6), "lon": round(lon, 6),
                    "alt": parts[9], "status": "3D Fix (Direct)", "fix": int(parts[6])
                })
            except: pass

    def get_location(self):
        return self.data
