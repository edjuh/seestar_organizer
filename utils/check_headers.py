#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Filename: utils/check_headers.py
# Purpose:  Utility to verify all project Python files contain a Purpose header.
# -----------------------------------------------------------------------------

import os
import glob

def check_headers(base_dir):
    # Find all Python files recursively
    search_pattern = os.path.join(base_dir, '**/*.py')
    py_files = glob.glob(search_pattern, recursive=True)
    
    missing_headers = []

    for filepath in py_files:
        # Ignore virtual environments and cache directories
        if 'venv' in filepath or '.pyenv' in filepath or '__pycache__' in filepath:
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if '# Purpose:' not in content:
                missing_headers.append(filepath)
    
    print("\n=== Header Verification Report ===")
    if missing_headers:
        print("❌ The following files are missing the '# Purpose:' tag:")
        for missing in missing_headers:
            print(f"  - {os.path.relpath(missing, base_dir)}")
    else:
        print("✅ All project Python files have their '# Purpose:' tags! The library is pristine.")
    print("==================================\n")

if __name__ == "__main__":
    # Point it at the project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    check_headers(project_root)
