import threading
import time
import socket
import json
from .env_loader import cfg

class GPSSensor:
    def __init__(self):
        self.fallback_lat = cfg("location", "lat", 52.38)
        self.fallback_lon = cfg("location", "lon", 4.64)
        
        self.state = {
            "lat": self.fallback_lat,
            "lon": self.fallback_lon,
            "fix": False,
            "sats_seen": 0,
            "sats_used": 0,
            "gps_time": None,
            "system_time": time.time()
        }
        self._lock = threading.Lock()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5.0)
                s.connect(("localhost", 2947))
                s.sendall(b'?WATCH={"enable":true,"json":true};\n')
                
                buffer = ""
                while True:
                    data = s.recv(4096).decode("utf-8")
                    if not data:
                        break
                    
                    buffer += data
                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        if not line.strip(): continue
                        
                        try:
                            msg = json.loads(line)
                            with self._lock:
                                if msg.get("class") == "TPV":
                                    mode = msg.get("mode", 0)
                                    self.state["gps_time"] = msg.get("time")
                                    self.state["system_time"] = time.time()
                                    
                                    if mode >= 2:
                                        self.state["lat"] = msg.get("lat", self.state["lat"])
                                        self.state["lon"] = msg.get("lon", self.state["lon"])
                                        self.state["fix"] = True
                                    else:
                                        self.state["fix"] = False
                                        
                                elif msg.get("class") == "SKY":
                                    sats = msg.get("satellites", [])
                                    self.state["sats_seen"] = len(sats)
                                    self.state["sats_used"] = sum(1 for sat in sats if sat.get("used", False))
                        except json.JSONDecodeError:
                            pass
                            
            except Exception:
                with self._lock:
                    self.state["fix"] = False
                time.sleep(2)

    def get_state(self):
        with self._lock:
            return self.state.copy()

# Singleton instance
gps_station = GPSSensor()
