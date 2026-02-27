#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Seestar Organizer - Pre-Flight Check
# Path: ~/seestar_organizer/core/flight/preflight_check.py
# Purpose: Executes full system validation including Targets, GPS, Bridge, Weather, and Disk.
# ----------------------------------------------------------------

import json
import os
import sys
import socket
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from core.flight.vault_manager import VaultManager
from core.preflight.weather import WeatherOracle
from core.utils.disk_monitor import DiskMonitor
from core.preflight.target_evaluator import TargetEvaluator

PREFLIGHT_DATA = os.path.expanduser("~/seestar_organizer/core/flight/data/preflight_status.json")

def get_gps_fix():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2.0)
            s.connect(('127.0.0.1', 2947))
            s.sendall(b'?WATCH={"enable":true,"json":true}\n')
            start = time.time()
            while time.time() - start < 2.0:
                data = s.recv(4096).decode('utf-8')
                for line in data.split('\n'):
                    if not line.strip(): continue
                    try:
                        msg = json.loads(line)
                        if msg.get('class') == 'TPV' and msg.get('mode', 0) >= 2:
                            return "OK", msg['lat'], msg['lon']
                    except json.JSONDecodeError: continue
        return "TRYING", 0.0, 0.0
    except Exception: return "BAD", 0.0, 0.0

def get_maidenhead(lat, lon):
    if lat == 0.0: return "WAITING"
    A, B = lon + 180, lat + 90
    mh = chr(ord('A')+int(A//20)) + chr(ord('A')+int(B//10)) + str(int((A%20)//2)) + str(int(B%10))
    return mh

def check_vitals():
    vault, oracle, disk_mon, target_eval = VaultManager(), WeatherOracle(), DiskMonitor(), TargetEvaluator()
    
    # 1. Hardware/Weather/Disk
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    bridge_ok = "OK" if s.connect_ex(('127.0.0.1', 5555)) == 0 else "BAD"
    s.close()

    gps_status, real_lat, real_lon = get_gps_fix()
    if gps_status == "OK":
        vault.sync_gps(real_lat, real_lon, get_maidenhead(real_lat, real_lon))

    weather_report = oracle.get_consensus()
    disk_report = disk_mon.check_vitals()
    target_report = target_eval.evaluate()
    obs = vault.get_observer_config()

    status = {
        "bridge": bridge_ok,
        "gps": gps_status,
        "weather": weather_report["status"], "weather_led": weather_report["led"],
        "disk": disk_report["status"], "disk_led": disk_report["led"],
        "targets": target_report["status"], "targets_led": target_report["led"],
        "location_maidenhead": obs.get("maidenhead", "ERR"),
        "observer_id": obs.get("observer_id", "ERR"),
        "jd": round(2440587.5 + time.time() / 86400.0, 4)
    }

    os.makedirs(os.path.dirname(PREFLIGHT_DATA), exist_ok=True)
    with open(PREFLIGHT_DATA, 'w') as f: json.dump(status, f)
        
    print("\n🚀 === PRE-FLIGHT VITALS REPORT ===")
    print(f"   GPS / BRIDGE     : {status['gps']} / {status['bridge']}")
    print(f"   WEATHER (PRED)   : {status['weather']}")
    print(f"   DISK STORAGE     : {status['disk']}")
    print(f"   TARGET MANIFEST  : {status['targets']}")
    print("===================================\n")

if __name__ == "__main__":
    check_vitals()
