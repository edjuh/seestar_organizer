#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: test_darkness.py
Version: 1.2.0 (Pee Pastinakel)
Objective: Performs high-precision validation of astronomical darkness windows using coordinate data from the VaultManager.
"""

import sys
import os
import ephem

# Import your real config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.flight.vault_manager import VaultManager

def test_twilight():
    vault = VaultManager()
    obs_config = vault.get_observer_config()
    
    # Setup Ephem Observer using ONLY Vault data
    observer = ephem.Observer()
    observer.lat = str(obs_config["lat"])
    observer.lon = str(obs_config["lon"])
    observer.elevation = float(obs_config["elevation"])
    observer.horizon = str(obs_config["sun_altitude_limit"])
    
    try:
        astro_dusk = observer.next_setting(ephem.Sun(), use_center=True)
        astro_dawn = observer.next_rising(ephem.Sun(), use_center=True)
        
        print("\n🔭 === STRICT ASTRONOMICAL DARKNESS TEST ===")
        print(f"Location Config : {observer.lat} N, {observer.lon} E")
        print(f"Elevation       : {observer.elevation} m")
        print(f"Sun Alt Limit   : {observer.horizon}°")
        print(f"Astro Dusk      : {ephem.localtime(astro_dusk).strftime('%Y-%m-%d %H:%M:%S')} Local Time")
        print(f"Astro Dawn      : {ephem.localtime(astro_dawn).strftime('%Y-%m-%d %H:%M:%S')} Local Time")
        print("============================================\n")
        
    except ephem.AlwaysUpError:
        print(f"\n⚠️ WARNING: The sun does not reach {observer.horizon}° at this location tonight.")
    except ephem.NeverUpError:
        print("\n⚠️ WARNING: Polar night conditions.")

if __name__ == "__main__":
    test_twilight()
