#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: utils/check_headers.py
Version: 1.2.0 (Pee Pastinakel)
Objective: Utility to verify all project Python files contain a standardized PEP 257 header.
"""

import os
import glob

def check_headers(base_dir):
    search_pattern = os.path.join(base_dir, '**/*.py')
    py_files = glob.glob(search_pattern, recursive=True)
    missing_headers = []

    for filepath in py_files:
        if any(x in filepath for x in ['venv', '.pyenv', '__pycache__']):
            continue
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read(1000)
            if 'Filename:' not in content:
                missing_headers.append(filepath)
    
    print("\n=== Header Verification Report ===")
    if missing_headers:
        for missing in missing_headers:
            print(f"  - {os.path.relpath(missing, base_dir)}")
    else:
        print("✅ All files standardized.")
    print("==================================\n")

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    check_headers(project_root)
