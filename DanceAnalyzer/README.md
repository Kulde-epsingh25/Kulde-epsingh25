# 💃 Dance Analyzer — ML Dataset Structure

> A large-scale, MediaPipe pose-based dance recognition dataset covering **39 dance types** across **6 categories**.  
> Designed for a final-year machine-learning project.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Complete Folder Tree](#complete-folder-tree)
3. [Dance Categories & Recommendations](#dance-categories--recommendations)
4. [MediaPipe Pose Keypoints](#mediapipe-pose-keypoints)
5. [Keypoints CSV Format](#keypoints-csv-format)
6. [Annotation JSON Format](#annotation-json-format)
7. [File Naming Conventions](#file-naming-conventions)
8. [Dataset Splits](#dataset-splits)
9. [Quick Start](#quick-start)
10. [Scripts Reference](#scripts-reference)

---

## Project Overview

| Property               | Value                              |
|------------------------|------------------------------------|
| Pose Model             | MediaPipe BlazePose (33 landmarks) |
| Input Resolution       | 640 × 480 px                       |
| Target FPS             | 30                                 |
| Sequence Length        | 30 frames                          |
| Frame Overlap          | 10 frames                          |
| Total Dance Types      | 39                                 |
| Categories             | 6                                  |
| Split Ratio            | 70 % train / 15 % val / 15 % test  |
| Keypoint Array Shape   | `[30, 33, 4]` per sequence         |
| Coord Order            | `[x, y, z, visibility]`            |

---

## Complete Folder Tree

```
DanceAnalyzer/
├── README.md                          ← This file
│
├── dataset/
│   │
│   ├── videos/                        ← Source & processed video files
│   │   │
│   │   ├── indian_classical/
│   │   │   ├── bharatanatyam/
│   │   │   │   ├── raw_videos/        ← Original downloaded .mp4 files
│   │   │   │   ├── processed_videos/  ← Resized, trimmed, normalised
│   │   │   │   ├── frames/            ← Per-video JPEG frame sets
│   │   │   │   ├── keypoints/         ← Per-frame .npy keypoint arrays
│   │   │   │   ├── annotations/       ← Per-video JSON annotation files
│   │   │   │   └── sample_sequences/  ← Ready-to-train 30-frame .npy seqs
│   │   │   ├── kathak/
│   │   │   │   ├── raw_videos/
│   │   │   │   ├── processed_videos/
│   │   │   │   ├── frames/
│   │   │   │   ├── keypoints/
│   │   │   │   ├── annotations/
│   │   │   │   └── sample_sequences/
│   │   │   ├── odissi/         (same 6-subfolder structure)
│   │   │   ├── kuchipudi/      (same 6-subfolder structure)
│   │   │   ├── mohiniyattam/   (same 6-subfolder structure)
│   │   │   ├── manipuri/       (same 6-subfolder structure)
│   │   │   ├── kathakali/      (same 6-subfolder structure)
│   │   │   └── sattriya/       (same 6-subfolder structure)
│   │   │
│   │   ├── indian_folk/
│   │   │   ├── bhangra/        (same 6-subfolder structure)
│   │   │   ├── garba/          (same 6-subfolder structure)
│   │   │   ├── ghoomar/        (same 6-subfolder structure)
│   │   │   ├── bihu/           (same 6-subfolder structure)
│   │   │   ├── lavani/         (same 6-subfolder structure)
│   │   │   ├── kalbelia/       (same 6-subfolder structure)
│   │   │   ├── chhau/          (same 6-subfolder structure)
│   │   │   └── yakshagana/     (same 6-subfolder structure)
│   │   │
│   │   ├── western_street/
│   │   │   ├── hip_hop/        (same 6-subfolder structure)
│   │   │   ├── breakdance/     (same 6-subfolder structure)
│   │   │   ├── popping/        (same 6-subfolder structure)
│   │   │   ├── locking/        (same 6-subfolder structure)
│   │   │   ├── krumping/       (same 6-subfolder structure)
│   │   │   └── street/         (same 6-subfolder structure)
│   │   │
│   │   ├── contemporary_modern/
│   │   │   ├── contemporary/   (same 6-subfolder structure)
│   │   │   ├── modern/         (same 6-subfolder structure)
│   │   │   ├── lyrical/        (same 6-subfolder structure)
│   │   │   ├── jazz/           (same 6-subfolder structure)
│   │   │   └── ballet/         (same 6-subfolder structure)
│   │   │
│   │   ├── latin_ballroom/
│   │   │   ├── salsa/          (same 6-subfolder structure)
│   │   │   ├── tango/          (same 6-subfolder structure)
│   │   │   ├── waltz/          (same 6-subfolder structure)
│   │   │   ├── cha_cha/        (same 6-subfolder structure)
│   │   │   ├── rumba/          (same 6-subfolder structure)
│   │   │   ├── samba/          (same 6-subfolder structure)
│   │   │   └── jive/           (same 6-subfolder structure)
│   │   │
│   │   └── commercial_social/
│   │       ├── bollywood/      (same 6-subfolder structure)
│   │       ├── k_pop/          (same 6-subfolder structure)
│   │       ├── freestyle/      (same 6-subfolder structure)
│   │       ├── party/          (same 6-subfolder structure)
│   │       └── zumba/          (same 6-subfolder structure)
│   │
│   ├── extracted_frames/              ← All JPEG frames, mirroring videos/
│   │   ├── indian_classical/
│   │   │   ├── bharatanatyam/
│   │   │   │   └── bharatanatyam_v001/
│   │   │   │       ├── bharatanatyam_v001_f0001.jpg
│   │   │   │       ├── bharatanatyam_v001_f0002.jpg
│   │   │   │       └── ...
│   │   │   └── kathak/ ...
│   │   ├── indian_folk/ ...
│   │   ├── western_street/ ...
│   │   ├── contemporary_modern/ ...
│   │   ├── latin_ballroom/ ...
│   │   └── commercial_social/ ...
│   │
│   ├── pose_keypoints/                ← .npy sequence files, mirroring videos/
│   │   ├── indian_classical/
│   │   │   ├── bharatanatyam/
│   │   │   │   ├── bharatanatyam_v001_seq001.npy   ← shape [30, 33, 4]
│   │   │   │   ├── bharatanatyam_v001_seq002.npy
│   │   │   │   └── ...
│   │   │   └── kathak/ ...
│   │   ├── indian_folk/ ...
│   │   ├── western_street/ ...
│   │   ├── contemporary_modern/ ...
│   │   ├── latin_ballroom/ ...
│   │   └── commercial_social/ ...
│   │
│   ├── splits/
│   │   ├── train_manifest.csv         ← sequence_file, label_id, dance_type, …
│   │   ├── val_manifest.csv
│   │   ├── test_manifest.csv
│   │   ├── train/                     ← Symlinks or copies (optional)
│   │   │   └── {category}/{dance}/
│   │   ├── val/
│   │   │   └── {category}/{dance}/
│   │   └── test/
│   │       └── {category}/{dance}/
│   │
│   └── metadata/
│       ├── labels.json                ← label_id → dance_name mapping
│       ├── class_mapping.csv          ← Full class details + recommendations
│       └── dataset_info.json          ← Project-level config & MediaPipe settings
│
├── examples/
│   ├── sample_keypoints.csv           ← One-row example of keypoint CSV
│   ├── sample_annotation.json         ← Full per-video annotation example
│   └── naming_conventions.md          ← Detailed file-naming rules
│
└── scripts/
    ├── setup_dataset.py               ← Creates all directories
    ├── extract_keypoints.py           ← MediaPipe extraction → .npy
    └── build_splits.py                ← Generates train/val/test manifests
```

---

## Dance Categories & Recommendations

### 🕺 Indian Classical  *(8 types)*

| Dance Type     | Label ID | Min Videos | Rec. Videos | Frames/Video | Sequences |
|----------------|----------|-----------|-------------|--------------|-----------|
| Bharatanatyam  | 0        | 100       | 150         | 30           | 4 500     |
| Kathak         | 1        | 100       | 150         | 30           | 4 500     |
| Odissi         | 2        | 100       | 150         | 30           | 4 500     |
| Kuchipudi      | 3        | 100       | 150         | 30           | 4 500     |
| Mohiniyattam   | 4        | 75        | 100         | 30           | 3 000     |
| Manipuri       | 5        | 75        | 100         | 30           | 3 000     |
| Kathakali      | 6        | 75        | 100         | 30           | 3 000     |
| Sattriya       | 7        | 75        | 100         | 30           | 3 000     |

### 🎊 Indian Folk  *(8 types)*

| Dance Type | Label ID | Rec. Videos | Sequences |
|------------|----------|-------------|-----------|
| Bhangra    | 8        | 200         | 6 000     |
| Garba      | 9        | 200         | 6 000     |
| Ghoomar    | 10       | 150         | 4 500     |
| Bihu       | 11       | 150         | 4 500     |
| Lavani     | 12       | 150         | 4 500     |
| Kalbelia   | 13       | 100         | 3 000     |
| Chhau      | 14       | 100         | 3 000     |
| Yakshagana | 15       | 100         | 3 000     |

### 🤸 Western Street  *(6 types)*

| Dance Type | Label ID | Rec. Videos | Sequences |
|------------|----------|-------------|-----------|
| Hip-Hop    | 16       | 250         | 7 500     |
| Breakdance | 17       | 250         | 7 500     |
| Popping    | 18       | 200         | 6 000     |
| Locking    | 19       | 200         | 6 000     |
| Krumping   | 20       | 150         | 4 500     |
| Street     | 21       | 150         | 4 500     |

### 🩰 Contemporary / Modern  *(5 types)*

| Dance Type    | Label ID | Rec. Videos | Sequences |
|---------------|----------|-------------|-----------|
| Contemporary  | 22       | 200         | 6 000     |
| Modern        | 23       | 200         | 6 000     |
| Lyrical       | 24       | 150         | 4 500     |
| Jazz          | 25       | 150         | 4 500     |
| Ballet        | 26       | 200         | 6 000     |

### 💃 Latin / Ballroom  *(7 types)*

| Dance Type | Label ID | Rec. Videos | Sequences |
|------------|----------|-------------|-----------|
| Salsa      | 27       | 200         | 6 000     |
| Tango      | 28       | 200         | 6 000     |
| Waltz      | 29       | 150         | 4 500     |
| Cha-Cha    | 30       | 150         | 4 500     |
| Rumba      | 31       | 150         | 4 500     |
| Samba      | 32       | 150         | 4 500     |
| Jive       | 33       | 100         | 3 000     |

### 🎤 Commercial / Social  *(5 types)*

| Dance Type | Label ID | Rec. Videos | Sequences |
|------------|----------|-------------|-----------|
| Bollywood  | 34       | 300         | 9 000     |
| K-Pop      | 35       | 300         | 9 000     |
| Freestyle  | 36       | 200         | 6 000     |
| Party      | 37       | 200         | 6 000     |
| Zumba      | 38       | 150         | 4 500     |

---

## MediaPipe Pose Keypoints

BlazePose detects **33 body landmarks**. Each landmark has 4 values:

```
[x, y, z, visibility]
```

| Index | Landmark           | Index | Landmark            |
|-------|--------------------|-------|---------------------|
| 0     | nose               | 17    | left_pinky          |
| 1     | left_eye_inner     | 18    | right_pinky         |
| 2     | left_eye           | 19    | left_index          |
| 3     | left_eye_outer     | 20    | right_index         |
| 4     | right_eye_inner    | 21    | left_thumb          |
| 5     | right_eye          | 22    | right_thumb         |
| 6     | right_eye_outer    | 23    | left_hip            |
| 7     | left_ear           | 24    | right_hip           |
| 8     | right_ear          | 25    | left_knee           |
| 9     | mouth_left         | 26    | right_knee          |
| 10    | mouth_right        | 27    | left_ankle          |
| 11    | left_shoulder      | 28    | right_ankle         |
| 12    | right_shoulder     | 29    | left_heel           |
| 13    | left_elbow         | 30    | right_heel          |
| 14    | right_elbow        | 31    | left_foot_index     |
| 15    | left_wrist         | 32    | right_foot_index    |
| 16    | right_wrist        |       |                     |

**Sequence array shape**: `[30 frames, 33 landmarks, 4 coords]` → flattened to `[30, 132]` for LSTM/GRU input.

---

## Keypoints CSV Format

Each row in a keypoints CSV represents **one frame**:

```
frame_id, video_id, dance_type, category, timestamp_ms,
nose_x, nose_y, nose_z, nose_v,
left_eye_inner_x, ..., right_foot_index_v,
label_id, split
```

See [`examples/sample_keypoints.csv`](examples/sample_keypoints.csv) for a full single-row example.

**Total columns**: 5 (meta) + 33 × 4 (keypoints) + 2 (label, split) = **139 columns**

---

## Annotation JSON Format

Each video has a `{dance_type}_v{NNN}_annotation.json` file:

```json
{
  "annotation_version": "1.0",
  "video_id": "bharatanatyam_v001",
  "dance_type": "bharatanatyam",
  "category": "indian_classical",
  "label_id": 0,
  "split": "train",
  "duration_seconds": 120.5,
  "fps": 30,
  "total_frames": 3615,
  "resolution": "640x480",
  "sequences": [
    {
      "sequence_id": "bharatanatyam_v001_seq001",
      "start_frame": 0,
      "end_frame": 29,
      "label_id": 0,
      "keypoints_file": "pose_keypoints/indian_classical/bharatanatyam/bharatanatyam_v001_seq001.npy",
      "pose_confidence_mean": 0.987
    }
  ],
  "mediapipe_settings": {
    "model_complexity": 1,
    "min_detection_confidence": 0.7,
    "min_tracking_confidence": 0.6
  }
}
```

See [`examples/sample_annotation.json`](examples/sample_annotation.json) for the full schema.

---

## File Naming Conventions

| File Type            | Pattern                                    | Example                             |
|----------------------|--------------------------------------------|-------------------------------------|
| Raw video            | `{dance}_v{NNN}.mp4`                       | `bharatanatyam_v001.mp4`            |
| Processed video      | `{dance}_v{NNN}_proc.mp4`                  | `bhangra_v012_proc.mp4`             |
| Frame image          | `{dance}_v{NNN}_f{FFFF}.jpg`               | `kathak_v005_f0001.jpg`             |
| Keypoint sequence    | `{dance}_v{NNN}_seq{SSS}.npy`              | `ballet_v007_seq001.npy`            |
| Per-frame keypoints  | `{dance}_v{NNN}_f{FFFF}_kp.npy`            | `breakdance_v003_f0045_kp.npy`      |
| Annotation           | `{dance}_v{NNN}_annotation.json`           | `tango_v011_annotation.json`        |
| Split manifest       | `{split}_manifest.csv`                     | `train_manifest.csv`                |

See [`examples/naming_conventions.md`](examples/naming_conventions.md) for complete rules.

---

## Dataset Splits

Split files are located at `dataset/splits/`:

```
dataset/splits/
├── train_manifest.csv   ← ~70% of video sequences
├── val_manifest.csv     ← ~15% of video sequences
└── test_manifest.csv    ← ~15% of video sequences
```

**Manifest CSV columns:**

```
sequence_file, label_id, dance_type, category, video_id, split
```

> ⚠️ Splits are stratified by **video** (not by sequence) to prevent data leakage.

---

## Quick Start

### 1. Create all directories

```bash
cd DanceAnalyzer
python scripts/setup_dataset.py --base-dir dataset
```

### 2. Add your raw videos

Place `.mp4` files under:
```
dataset/videos/{category}/{dance_type}/raw_videos/
```
Example: `dataset/videos/indian_classical/bharatanatyam/raw_videos/bharatanatyam_v001.mp4`

### 3. Extract MediaPipe keypoints

```bash
python scripts/extract_keypoints.py \
  --video-dir dataset/videos/indian_classical/bharatanatyam/raw_videos \
  --output-dir dataset/pose_keypoints/indian_classical/bharatanatyam \
  --label-id 0
```

### 4. Build train/val/test manifests

```bash
python scripts/build_splits.py --dataset-dir dataset
```

### 5. Train your model

Load sequences using the manifest:

```python
import numpy as np
import pandas as pd

train_df = pd.read_csv("dataset/splits/train_manifest.csv")
X, y = [], []
for _, row in train_df.iterrows():
    seq = np.load(row["sequence_file"])          # shape [30, 33, 4]
    X.append(seq.reshape(30, -1))                # flatten → [30, 132]
    y.append(row["label_id"])

X = np.array(X)   # [N, 30, 132]
y = np.array(y)   # [N]
```

---

## Scripts Reference

| Script                  | Purpose                                                 |
|-------------------------|---------------------------------------------------------|
| `setup_dataset.py`      | Creates the full directory tree with `.gitkeep` files   |
| `extract_keypoints.py`  | Runs MediaPipe on videos → saves `.npy` sequence arrays |
| `build_splits.py`       | Scans `pose_keypoints/` → writes manifest CSV files     |

---

## Requirements

```
mediapipe>=0.10.0
opencv-python>=4.8.0
numpy>=1.24.0
pandas>=2.0.0
```

Install with:
```bash
pip install mediapipe opencv-python numpy pandas
```

---

*Dance Analyzer — Final Year ML Project | Dataset v1.0.0*
