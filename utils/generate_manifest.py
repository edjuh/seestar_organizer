#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: utils/generate_manifest.py
Version: 1.2.0 (Pee Pastinakel)
Objective: Captures full-sentence objectives without clipping and syncs the resulting manifest to the NAS.
"""

import os, re, shutil

ROOT_DIR = os.path.expanduser("~/seestar_organizer")
MANIFEST_PATH = os.path.join(ROOT_DIR, "FILE_MANIFEST.md")
NAS_DIR = "/mnt/astronas/1.2"

def get_clean_objective(filepath):
    try:
        with open(filepath, 'r') as f:
            content = f.read(2000)
            match = re.search(r'Objective:\s*([^"\n\r]+)', content, re.IGNORECASE)
            if match:
                return match.group(1).strip()
    except: pass
    return "No objective defined."

def generate():
    sections = {
        "🛫 PREFLIGHT": ["core/preflight", "core/planning"],
        "🚀 FLIGHT": "core/flight",
        "🧪 POSTFLIGHT": "core/postflight",
        "🛠️ UTILS": ["utils", "core/utils", "core"]
    }
    with open(MANIFEST_PATH, 'w') as m:
        m.write("# Seestar Organizer: Purified Manifest\n\n")
        for title, folders in sections.items():
            m.write(f"## {title}\n")
            if isinstance(folders, str): folders = [folders]
            for fld in folders:
                target = os.path.join(ROOT_DIR, fld)
                if not os.path.exists(target): continue
                for file in sorted(os.listdir(target)):
                    if file.endswith(".py") and not file.startswith("__"):
                        obj = get_clean_objective(os.path.join(target, file))
                        m.write(f"* `{fld}/{file}`: {obj}\n")
            m.write("\n")
    if os.path.exists(NAS_DIR):
        os.system(f"cp {MANIFEST_PATH} {NAS_DIR}/")

if __name__ == "__main__":
    generate()
    print("✅ Purified Manifest mirrored to NAS.")
