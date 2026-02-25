#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: core/preflight/horizon.py
Version: 1.0.0 (Kwetal)
Role: Utility - Obstruction Mapper
Objective: Veto targets based on local obstructions (Trees, Buildings) using Az/Alt mapping.
"""

# Simple Azimuth: Min_Alt map for Haarlem obstructions
OBSTRUCTIONS = [
    {"az_start": 150, "az_end": 210, "min_alt": 45}, # Roof obstruction
    {"az_start": 300, "az_end": 350, "min_alt": 55}, # Tree in NW
]

def is_obstructed(az, alt):
    for obs in OBSTRUCTIONS:
        if obs["az_start"] <= az <= obs["az_end"]:
            if alt < obs["min_alt"]:
                return True
    return False
