"""
Dance Analyzer — Dataset Setup Script
======================================
Generates the complete folder structure for the Dance Analyzer dataset.
Run this script once to create all required directories.

Usage:
    python scripts/setup_dataset.py [--base-dir ./dataset]
"""

import os
import json
import argparse

# ─── Dance taxonomy ────────────────────────────────────────────────────────────
CATEGORIES = {
    "indian_classical": [
        "bharatanatyam", "kathak", "odissi", "kuchipudi",
        "mohiniyattam", "manipuri", "kathakali", "sattriya",
    ],
    "indian_folk": [
        "bhangra", "garba", "ghoomar", "bihu",
        "lavani", "kalbelia", "chhau", "yakshagana",
    ],
    "western_street": [
        "hip_hop", "breakdance", "popping", "locking", "krumping", "street",
    ],
    "contemporary_modern": [
        "contemporary", "modern", "lyrical", "jazz", "ballet",
    ],
    "latin_ballroom": [
        "salsa", "tango", "waltz", "cha_cha", "rumba", "samba", "jive",
    ],
    "commercial_social": [
        "bollywood", "k_pop", "freestyle", "party", "zumba",
    ],
}

DANCE_SUBFOLDERS = [
    "raw_videos",
    "processed_videos",
    "frames",
    "keypoints",
    "annotations",
    "sample_sequences",
]

SPLITS = ["train", "val", "test"]


# ─── Helpers ───────────────────────────────────────────────────────────────────
def make_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)
    gitkeep = os.path.join(path, ".gitkeep")
    if not os.path.exists(gitkeep):
        open(gitkeep, "w").close()


def build_structure(base: str) -> None:
    print(f"Building dataset structure under: {os.path.abspath(base)}\n")

    # 1. videos/ — full per-dance subfolder tree
    for category, dances in CATEGORIES.items():
        for dance in dances:
            for sub in DANCE_SUBFOLDERS:
                make_dir(os.path.join(base, "videos", category, dance, sub))

    # 2. extracted_frames/
    for category, dances in CATEGORIES.items():
        for dance in dances:
            make_dir(os.path.join(base, "extracted_frames", category, dance))

    # 3. pose_keypoints/
    for category, dances in CATEGORIES.items():
        for dance in dances:
            make_dir(os.path.join(base, "pose_keypoints", category, dance))

    # 4. splits/
    for split in SPLITS:
        for category, dances in CATEGORIES.items():
            for dance in dances:
                make_dir(os.path.join(base, "splits", split, category, dance))

    # 5. metadata/
    make_dir(os.path.join(base, "metadata"))

    print("✅  All directories created successfully.")
    _print_summary(base)


def _print_summary(base: str) -> None:
    total_dirs = sum(
        len(dirnames)
        for _, dirnames, _ in os.walk(base)
    )
    print(f"\n📁  Total directories created : {total_dirs}")
    total_classes = sum(len(v) for v in CATEGORIES.values())
    print(f"💃  Total dance types          : {total_classes}")
    print(f"📂  Categories                 : {len(CATEGORIES)}")


# ─── Entry point ───────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(description="Set up Dance Analyzer dataset directories.")
    parser.add_argument(
        "--base-dir",
        default=os.path.join(os.path.dirname(__file__), "..", "dataset"),
        help="Root directory for the dataset (default: ../dataset)",
    )
    args = parser.parse_args()
    build_structure(args.base_dir)


if __name__ == "__main__":
    main()
