#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: utils/undo_header_mess.py
Version: 1.2.0 (Pee Pastinakel)
Objective: Emergency recovery script to strip failed header automation attempts and restore file integrity.
"""

import os
import glob

def revert_mess(base_dir):
    search_pattern = os.path.join(base_dir, '**/*.py')
    py_files = glob.glob(search_pattern, recursive=True)
    fixed_count = 0

    for filepath in py_files:
        if any(x in filepath for x in ['venv', '.pyenv', '__pycache__']):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        if any("[TODO: Define the single responsibility" in line for line in lines):
            clean_lines = lines[7:]
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(clean_lines)
            rel_path = os.path.relpath(filepath, base_dir)
            print(f"🧹 Cleaned up: {rel_path}")
            fixed_count += 1

    print(f"\nDone! Reverted {fixed_count} files.")

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    revert_mess(project_root)
