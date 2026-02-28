#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: core/sequence_repository.py
Version: 1.2.0 (Pee Pastinakel)
Objective: Local cache manager for AAVSO V-band comparison sequences, reducing API overhead for offline planning.
"""

import json
from pathlib import Path

class SequenceRepository:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"
        self.seq_dir = self.data_dir / "sequences"
        self.seq_dir.mkdir(exist_ok=True)

    def get_sequence(self, star_name):
        safe_name = star_name.replace(" ", "_").lower() + ".json"
        file_path = self.seq_dir / safe_name
        if file_path.exists():
            with open(file_path, 'r') as f:
                return json.load(f)
        return None

    def load_targets(self):
        with open(self.data_dir / "targets.json", 'r') as f:
            return json.load(f)

if __name__ == "__main__":
    repo = SequenceRepository()
    print(f"✅ Sequence Repository: Initialized at {repo.seq_dir}")
