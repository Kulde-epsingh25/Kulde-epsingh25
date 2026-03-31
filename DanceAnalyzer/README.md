# 💃 Dance Analyzer — ML Dataset Structure

> A large-scale, pose-based dance recognition dataset covering **39 dance types** across **6 categories**.  
> Supports **three pose backends** — MediaPipe Holistic (body + both hands), MediaPipe BlazePose, and MoveNet (TF Hub).  
> Designed for a final-year machine-learning project.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Pose Backends](#pose-backends)
3. [Reference Repositories](#reference-repositories)
4. [Complete Folder Tree](#complete-folder-tree)
5. [Dance Categories & Recommendations](#dance-categories--recommendations)
6. [Keypoint Layouts by Backend](#keypoint-layouts-by-backend)
7. [Keypoints CSV Format](#keypoints-csv-format)
8. [Annotation JSON Format](#annotation-json-format)
9. [File Naming Conventions](#file-naming-conventions)
10. [Dataset Splits](#dataset-splits)
11. [Raw Image Support](#raw-image-support)
12. [Quick Start](#quick-start)
13. [Scripts Reference](#scripts-reference)

---

## Project Overview

| Property               | Value                                                   |
|------------------------|---------------------------------------------------------|
| Pose Backends          | MediaPipe Holistic · BlazePose · MoveNet (TF Hub)       |
| Input Resolution       | 640 × 480 px                                            |
| Target FPS             | 30                                                      |
| Sequence Length        | 30 frames                                               |
| Frame Overlap          | 10 frames                                               |
| Total Dance Types      | 39                                                      |
| Categories             | 6                                                       |
| Split Ratio            | 70 % train / 15 % val / 15 % test                       |
| Holistic Array Shape   | `[30, 75, 4]` — body(33)+L-hand(21)+R-hand(21)         |
| BlazePose Array Shape  | `[30, 33, 4]` — body only                               |
| MoveNet Array Shape    | `[30, 17, 3]` — COCO 17 keypoints                       |
| Coord Order            | `[x, y, z, visibility]` (holistic/mediapipe)            |
|                        | `[x, y, score]` (movenet)                               |

---

## Pose Backends

### 🤲 Holistic (Recommended for Indian Classical)

Uses **MediaPipe Holistic** to extract body landmarks **and** both hand
skeletons simultaneously.  
Hand mudras (hasta gestures) are the primary semantic unit of Bharatanatyam,
Kathak, Odissi and other classical forms — capturing them dramatically
improves model accuracy.

| Region | Landmarks | Indices in array |
|--------|-----------|-----------------|
| Body   | 33        | 0 – 32          |
| Left hand | 21   | 33 – 53         |
| Right hand | 21  | 54 – 74         |
| **Total** | **75** |                |

Output array shape: `[seq_len, 75, 4]`  
Install: `pip install mediapipe opencv-python`

### 🏃 MediaPipe (Body-only)

Original BlazePose body pipeline — 33 landmarks, no hand detail.  
Suitable for folk/street/ballroom dance where footwork and body posture are
the dominant features.  
Output array shape: `[seq_len, 33, 4]`

### ⚡ MoveNet (TF Hub)

Google's **MoveNet Thunder** / **Lightning** models via TF Hub.  
17 COCO keypoints — extremely fast on GPU.  
Use when you need rapid batch extraction of a very large video collection.

| Variant   | Input size | Speed  | Accuracy |
|-----------|-----------|--------|----------|
| Lightning | 192 × 192 | ★★★★★ | ★★★☆☆   |
| Thunder   | 256 × 256 | ★★★★☆ | ★★★★☆   |

Output array shape: `[seq_len, 17, 3]`  
Install: `pip install tensorflow tensorflow-hub`

### 🏆 MMPose — RTMPose (Highest Accuracy)

**[MMPose](https://github.com/open-mmlab/mmpose)** by OpenMMLab provides the
most accurate pose models available.  
The `wholebody` alias loads **RTMPose-Wholebody** which detects **133
COCO-WholeBody keypoints** in a single forward pass — body, feet, face
*and* both hands — making it the gold standard for Indian Classical dance
analysis where mudras and bhava (facial expressions) both carry meaning.

| Model alias | Keypoints | Best for                          |
|-------------|-----------|-----------------------------------|
| `wholebody` | 133       | Indian Classical (body+hands+face)|
| `human`     | 17 (COCO) | Folk / Street / Ballroom          |

Output array shape: `[seq_len, 133, 3]` (wholebody) or `[seq_len, 17, 3]` (human)  
Install:
```bash
pip install openmim
mim install mmengine "mmcv>=2.0.0" "mmdet>=3.0.0" "mmpose>=1.0.0"
```

---

## Reference Repositories

The following state-of-the-art repositories informed the design of this
pipeline. Reviewing them is strongly recommended before training models.

| Repository | What it offers |
|------------|---------------|
| [**MMPose** (OpenMMLab)](https://github.com/open-mmlab/mmpose) | Production-grade toolbox; RTMPose-Wholebody **133 keypoints** — integrated as `--backend mmpose` |
| [**MoveNet** (TF Hub)](https://tfhub.dev/s?q=movenet) | Ultra-fast TF Hub models; Lightning runs 30+ FPS on CPU |
| [**MoveNet tutorial** (TF Docs)](https://github.com/tensorflow/docs/blob/master/site/en/hub/tutorials/movenet.ipynb) | Official colab showing crop-region tracking for video |
| [**AlphaPose** (SJTU)](https://github.com/MVIG-SJTU/AlphaPose) | Multi-person tracking + wholebody (face+hand+foot); HybrIK for 3D mesh |
| [**ViTPose**](https://github.com/ViTAE-Transformer/ViTPose) | Vision-Transformer backbone, SOTA accuracy on COCO |
| [**RTMPose**](https://github.com/open-mmlab/mmpose/tree/main/projects/rtmpose) | Real-time 130 FPS multi-person, wholebody variant available |
| [**RTMO**](https://github.com/open-mmlab/mmpose/tree/main/projects/rtmo) | One-stage real-time multi-person — no separate detector needed |
| [**RTMW3D**](https://github.com/open-mmlab/mmpose/tree/main/projects/rtmpose3d) | Real-time 3D wholebody pose — future 3D dance analysis |

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
│   ├── raw_images/                    ← Optional still-image datasets by class
│   │   ├── indian_classical/
│   │   │   ├── bharatanatyam/
│   │   │   │   ├── bharatanatyam_img001.jpg
│   │   │   │   ├── bharatanatyam_img002.jpg
│   │   │   │   └── ...
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
    ├── extract_keypoints.py           ← Multi-backend extraction (mediapipe/holistic/movenet) → .npy
    ├── extract_gestures.py            ← Long-video motion-aware gesture extractor
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

## Keypoint Layouts by Backend

### Holistic — `[seq_len, 75, 4]` *(recommended for Indian Classical)*

Array indices: **0–32** BlazePose body · **33–53** Left hand · **54–74** Right hand.

Each value: `[x, y, z, visibility]`  
Flatten to `[seq_len, 300]` for LSTM/GRU input.

#### Body landmarks (indices 0 – 32, same as BlazePose)

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

#### Hand landmarks (indices 33–74)

Each hand has 21 landmarks (WRIST + 4 fingers × 5 joints).  
Left hand: indices **33–53** · Right hand: indices **54–74**

| Offset | Joint          |
|--------|----------------|
| 0      | WRIST          |
| 1–4    | THUMB (CMC→TIP)|
| 5–8    | INDEX finger   |
| 9–12   | MIDDLE finger  |
| 13–16  | RING finger    |
| 17–20  | PINKY finger   |

### MediaPipe (body-only) — `[seq_len, 33, 4]`

Same body landmarks as Holistic table above.  
Flatten to `[seq_len, 132]` for LSTM/GRU input.

### MoveNet — `[seq_len, 17, 3]`

COCO 17 keypoints · each value: `[x, y, score]`

| Index | Keypoint       | Index | Keypoint        |
|-------|----------------|-------|-----------------|
| 0     | nose           | 9     | left_wrist      |
| 1     | left_eye       | 10    | right_wrist     |
| 2     | right_eye      | 11    | left_hip        |
| 3     | left_ear       | 12    | right_hip       |
| 4     | right_ear      | 13    | left_knee       |
| 5     | left_shoulder  | 14    | right_knee      |
| 6     | right_shoulder | 15    | left_ankle      |
| 7     | left_elbow     | 16    | right_ankle     |
| 8     | right_elbow    |       |                 |

Flatten to `[seq_len, 51]` for LSTM/GRU input.

### MMPose wholebody — `[seq_len, 133, 3]`

COCO-WholeBody 133 keypoints · each value: `[x_norm, y_norm, score]`

| Indices  | Region          | Count | Notes                                    |
|----------|-----------------|-------|------------------------------------------|
| 0 – 16   | Body (COCO 17)  | 17    | Same order as MoveNet above              |
| 17 – 22  | Feet            | 6     | left_big_toe, left_small_toe, left_heel, right × 3 |
| 23 – 90  | Face            | 68    | 68 facial landmarks (eyes, nose, mouth, contour) |
| 91 – 111 | Left hand       | 21    | WRIST + 4 fingers × 5 joints            |
| 112 – 132| Right hand      | 21    | WRIST + 4 fingers × 5 joints            |

Flatten to `[seq_len, 399]` for LSTM/GRU input.  
Use `--backend mmpose --mmpose-model wholebody` to extract this layout.

### MMPose human — `[seq_len, 17, 3]`

Same COCO 17 keypoints as MoveNet, but extracted with RTMPose backbone
(higher accuracy).  Flatten to `[seq_len, 51]`.

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

## Raw Image Support

You can also include class-wise still images (e.g., Kaggle pose images) as an **auxiliary** source.

Put images under:

```
dataset/raw_images/{category}/{dance_type}/
```

Then extract pose sequences directly from those ordered images:

```bash
python scripts/extract_keypoints.py \
  --image-dir dataset/raw_images/indian_classical/bharatanatyam \
  --output-dir dataset/pose_keypoints/indian_classical/bharatanatyam \
  --label-id 0
```

Notes:

- `extract_keypoints.py` accepts **one** source at a time: `--video-dir` or `--image-dir`.
- Image data should support video-based data, not replace it, because temporal dynamics are weaker.

---

## Quick Start

### 1. Install dependencies

```bash
# Core (mediapipe / holistic backends)
pip install mediapipe opencv-python numpy pandas tqdm scipy

# Optional: MoveNet backend
pip install tensorflow tensorflow-hub
```

### 2. Create all directories

```bash
cd DanceAnalyzer
python scripts/setup_dataset.py --base-dir dataset
```

### 3. Add your raw videos

Place `.mp4` files under:
```
dataset/videos/{category}/{dance_type}/raw_videos/
```
Example: `dataset/videos/indian_classical/bharatanatyam/raw_videos/bharatanatyam_v001.mp4`

### 4a. Extract keypoints — standard videos

**Indian Classical — RTMPose-Wholebody 133 kpts (highest accuracy):**
```bash
python scripts/extract_keypoints.py \
  --video-dir dataset/videos/indian_classical/bharatanatyam/raw_videos \
  --output-dir dataset/pose_keypoints/indian_classical/bharatanatyam \
  --label-id 0 --backend mmpose --mmpose-model wholebody
```

**Indian Classical — Holistic (body + hands, no GPU required):**
```bash
python scripts/extract_keypoints.py \
  --video-dir dataset/videos/indian_classical/bharatanatyam/raw_videos \
  --output-dir dataset/pose_keypoints/indian_classical/bharatanatyam \
  --label-id 0 --backend holistic
```

**Body-only (folk / street / ballroom):**
```bash
python scripts/extract_keypoints.py \
  --video-dir dataset/videos/indian_folk/bhangra/raw_videos \
  --output-dir dataset/pose_keypoints/indian_folk/bhangra \
  --label-id 8 --backend mediapipe
```

**MoveNet Thunder (fast GPU extraction):**
```bash
python scripts/extract_keypoints.py \
  --video-dir dataset/videos/western_street/breakdance/raw_videos \
  --output-dir dataset/pose_keypoints/western_street/breakdance \
  --label-id 17 --backend movenet --movenet-variant thunder
```

**From raw images:**
```bash
python scripts/extract_keypoints.py \
  --image-dir dataset/raw_images/indian_classical/bharatanatyam \
  --output-dir dataset/pose_keypoints/indian_classical/bharatanatyam \
  --label-id 0 --backend mmpose --mmpose-model wholebody
```

### 4b. Extract gestures from long recordings

Use `extract_gestures.py` when your source videos are long stage recordings
(10 min – several hours). It detects active dance segments automatically and
skips static / transition passages, saving only meaningful sequences.

```bash
# One long video — MMPose Wholebody (highest accuracy)
python scripts/extract_gestures.py \
  --video dataset/videos/indian_classical/bharatanatyam/raw_videos/bharatanatyam_v001.mp4 \
  --output-dir dataset/pose_keypoints/indian_classical/bharatanatyam \
  --label-id 0 --backend mmpose --mmpose-model wholebody --min-motion 0.025

# One long video — Holistic (no GPU required)
python scripts/extract_gestures.py \
  --video dataset/videos/indian_classical/bharatanatyam/raw_videos/bharatanatyam_v001.mp4 \
  --output-dir dataset/pose_keypoints/indian_classical/bharatanatyam \
  --label-id 0 --backend holistic --min-motion 0.025

# Whole directory of long videos
python scripts/extract_gestures.py \
  --video-dir dataset/videos/indian_classical/kathak/raw_videos \
  --output-dir dataset/pose_keypoints/indian_classical/kathak \
  --label-id 1 --backend mmpose --mmpose-model wholebody
```

> **Tip:** For subtle Indian Classical movements lower `--min-motion` to `0.02`.
> For energetic styles (Bhangra, Breakdance) raise it to `0.05–0.08`.

### 5. Build train/val/test manifests

```bash
python scripts/build_splits.py --dataset-dir dataset
```

### 6. Train your model

Load sequences using the manifest:

```python
import numpy as np
import pandas as pd

train_df = pd.read_csv("dataset/splits/train_manifest.csv")
X, y = [], []
for _, row in train_df.iterrows():
    seq = np.load(row["sequence_file"])   # e.g. [30, 75, 4] holistic
    X.append(seq.reshape(seq.shape[0], -1))   # flatten → [30, 300]
    y.append(row["label_id"])

X = np.array(X)   # [N, 30, 300]  (holistic)  or [N, 30, 132] (mediapipe)
y = np.array(y)   # [N]
```

---

## Scripts Reference

| Script                   | Purpose                                                                             |
|--------------------------|-------------------------------------------------------------------------------------|
| `setup_dataset.py`       | Creates the full directory tree with `.gitkeep` files                               |
| `extract_keypoints.py`   | Multi-backend extractor (mediapipe / holistic / movenet) → `.npy` sequences         |
| `extract_gestures.py`    | **New** — long-video motion-aware gesture extractor with scene detection            |
| `build_splits.py`        | Scans `pose_keypoints/` → writes train/val/test manifest CSV files                  |

### `extract_keypoints.py` arguments

| Argument             | Default      | Description                                              |
|----------------------|--------------|----------------------------------------------------------|
| `--video-dir`        | —            | Directory of video files (mutually exclusive)            |
| `--image-dir`        | —            | Directory of ordered still images                        |
| `--output-dir`       | required     | Where to save `.npy` sequences                           |
| `--label-id`         | required     | Integer class label                                      |
| `--backend`          | `holistic`   | `mediapipe` / `holistic` / `movenet` / `mmpose`          |
| `--movenet-variant`  | `thunder`    | `lightning` or `thunder`                                 |
| `--mmpose-model`     | `wholebody`  | `wholebody` (133 kpts) or `human` (17 kpts)              |
| `--sequence-length`  | `30`         | Frames per sequence                                      |
| `--overlap`          | `10`         | Overlapping frames between sequences                     |
| `--min-confidence`   | `0.5`        | Minimum mean landmark confidence to keep a sequence      |

### `extract_gestures.py` arguments

All arguments from `extract_keypoints.py` plus:

| Argument          | Default | Description                                               |
|-------------------|---------|-----------------------------------------------------------|
| `--video`         | —       | Single video file path (mutually exclusive with --video-dir) |
| `--video-dir`     | —       | Directory of video files                                  |
| `--min-motion`    | `0.03`  | Motion threshold — skip near-static frames                |
| `--min-duration`  | `1.0`   | Minimum active-window duration in seconds                 |
| `--merge-gap`     | `0.5`   | Merge windows closer than this many seconds apart         |

---

## Requirements

```
mediapipe>=0.10.0
opencv-python>=4.8.0
numpy>=1.24.0
pandas>=2.0.0
tqdm>=4.65.0
scipy>=1.10.0             # gesture extractor
tensorflow>=2.12.0        # MoveNet only
tensorflow-hub>=0.13.0
mmpose>=1.0.0             # install via mim (see below)
```

Install core packages:
```bash
pip install mediapipe opencv-python numpy pandas tqdm scipy
```

Install MoveNet extras:
```bash
pip install tensorflow tensorflow-hub
```

Install MMPose (recommended for Indian Classical — highest accuracy):
```bash
pip install openmim
mim install mmengine "mmcv>=2.0.0" "mmdet>=3.0.0" "mmpose>=1.0.0"
```

---

*Dance Analyzer — Final Year ML Project | Dataset v1.0.0*
