#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: utils/inspect_comp.py
Version: 1.2.0 (Pee Pastinakel)
Objective: Visual validation utility to safely inspect comparison star coordinates and chart structures.
"""

import os
import json

d = '/home/ed/seestar_organizer/data/comp_stars'
files = [x for x in os.listdir(d) if x.endswith('.json')]

print(f"Total charts found: {len(files)}")

for f in files[:5]:
    try:
        data = json.load(open(os.path.join(d, f)))
        print(f"\n📄 {f}")
        
        if isinstance(data, list) and len(data) > 0:
            star = data
            if 'ra' in star and 'dec' in star:
                print(f"   ↳ RA: '{star['ra']}' (Type: {type(star['ra']).__name__})")
                print(f"   ↳ DEC: '{star['dec']}' (Type: {type(star['dec']).__name__})")
            else:
                print("   ↳ Missing 'ra' or 'dec' keys in the first star.")
        else:
            print(f"   ↳ Not a list or list is empty. Type: {type(data)}")
    except Exception as e:
        print(f"   ↳ ❌ Error parsing file: {e}")
