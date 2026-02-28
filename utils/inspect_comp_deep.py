#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: utils/inspect_comp_deep.py
Version: 1.2.0 (Pee Pastinakel)
Objective: Deep-dive diagnostic tool to inspect and preview raw JSON comparison star chart contents.
"""

import os
import json

d = '/home/ed/seestar_organizer/data/comp_stars'
files = [x for x in os.listdir(d) if x.endswith('.json')]

for f in files[:2]:
    try:
        data = json.load(open(os.path.join(d, f)))
        print(f"\n📄 {f}")
        
        if isinstance(data, list) and len(data) > 0:
            print(f"🔑 Keys found: {list(data.keys())}")
            print(f"📦 Raw preview: {data}")
        elif isinstance(data, dict):
            print(f"🔑 Dict Keys found: {list(data.keys())}")
    except Exception as e:
        print(f"❌ Error: {e}")
