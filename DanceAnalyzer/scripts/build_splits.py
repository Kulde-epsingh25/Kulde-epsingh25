"""
Dance Analyzer — Dataset Split Builder
========================================
Scans pose_keypoints/ for .npy sequences and writes
train / val / test manifest CSV files.

Usage:
    python scripts/build_splits.py \
        --dataset-dir dataset \
        --train 0.70 --val 0.15 --test 0.15 \
        --seed 42
"""

import os
import csv
import json
import random
import argparse
from pathlib import Path


def load_labels(metadata_dir: str) -> dict:
    labels_path = os.path.join(metadata_dir, "labels.json")
    with open(labels_path) as f:
        data = json.load(f)

    name_to_id = {}
    for cat_info in data["categories"].values():
        for label_id, dance_name in cat_info["classes"].items():
            name_to_id[dance_name] = int(label_id)
    return name_to_id


def gather_sequences(keypoints_root: str, name_to_id: dict) -> list:
    records = []
    kp_path = Path(keypoints_root)
    for category_dir in sorted(kp_path.iterdir()):
        if not category_dir.is_dir():
            continue
        for dance_dir in sorted(category_dir.iterdir()):
            if not dance_dir.is_dir():
                continue
            dance_name = dance_dir.name
            label_id = name_to_id.get(dance_name, -1)
            for npy_file in sorted(dance_dir.glob("*.npy")):
                # derive video_id from filename (everything before _seq or _f)
                stem = npy_file.stem
                video_id = stem.rsplit("_seq", 1)[0]
                records.append({
                    "sequence_file": str(npy_file.relative_to(kp_path.parent)),
                    "label_id": label_id,
                    "dance_type": dance_name,
                    "category": category_dir.name,
                    "video_id": video_id,
                })
    return records


def split_records(records: list, ratios: tuple, seed: int) -> tuple:
    random.seed(seed)
    # Group by video_id to avoid leaking frames across splits
    from collections import defaultdict
    by_video = defaultdict(list)
    for r in records:
        by_video[r["video_id"]].append(r)

    video_ids = list(by_video.keys())
    random.shuffle(video_ids)

    n = len(video_ids)
    n_train = int(n * ratios[0])
    n_val = int(n * ratios[1])

    train_ids = set(video_ids[:n_train])
    val_ids = set(video_ids[n_train : n_train + n_val])
    test_ids = set(video_ids[n_train + n_val :])

    train, val, test = [], [], []
    for vid_id, seqs in by_video.items():
        if vid_id in train_ids:
            train.extend(seqs)
        elif vid_id in val_ids:
            val.extend(seqs)
        else:
            test.extend(seqs)

    return train, val, test


FIELDNAMES = ["sequence_file", "label_id", "dance_type", "category", "video_id", "split"]


def write_manifest(records: list, split_name: str, output_dir: str) -> None:
    out_path = os.path.join(output_dir, f"{split_name}_manifest.csv")
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for r in records:
            writer.writerow({**r, "split": split_name})
    print(f"  {split_name:5s}: {len(records):6d} sequences → {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build train/val/test manifest CSVs.")
    parser.add_argument("--dataset-dir", default="dataset")
    parser.add_argument("--train", type=float, default=0.70)
    parser.add_argument("--val", type=float, default=0.15)
    parser.add_argument("--test", type=float, default=0.15)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    assert abs(args.train + args.val + args.test - 1.0) < 1e-6, "Ratios must sum to 1.0"

    metadata_dir = os.path.join(args.dataset_dir, "metadata")
    keypoints_root = os.path.join(args.dataset_dir, "pose_keypoints")
    splits_dir = os.path.join(args.dataset_dir, "splits")
    os.makedirs(splits_dir, exist_ok=True)

    name_to_id = load_labels(metadata_dir)
    records = gather_sequences(keypoints_root, name_to_id)

    if not records:
        print("⚠️  No .npy files found. Run extract_keypoints.py first.")
        return

    train, val, test = split_records(records, (args.train, args.val, args.test), args.seed)

    print(f"\nDataset split (seed={args.seed}):")
    write_manifest(train, "train", splits_dir)
    write_manifest(val, "val", splits_dir)
    write_manifest(test, "test", splits_dir)
    print(f"\n✅  Total sequences: {len(records)}")


if __name__ == "__main__":
    main()
