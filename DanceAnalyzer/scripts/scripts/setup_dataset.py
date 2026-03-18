#!/usr/bin/env python3
"""Workspace wrapper for DanceAnalyzer dataset setup."""

from pathlib import Path
import os
import runpy
import sys

TARGET = Path(__file__).resolve().parent.parent / "DanceAnalyzer" / "scripts" / "setup_dataset.py"
PROJECT_DIR = TARGET.parent.parent

if not TARGET.exists():
    raise SystemExit(f"Target script not found: {TARGET}")

os.chdir(PROJECT_DIR)
sys.path.insert(0, str(TARGET.parent))
runpy.run_path(str(TARGET), run_name="__main__")
