# File Naming Conventions — Dance Analyzer Dataset

## General Pattern

All files follow a consistent naming pattern to ensure automated parsing:

```
{dance_type}_{source_id}_{sequence/frame_number}.{ext}
```

---

## Videos

### Raw Videos
```
{dance_type}_v{NNN}.mp4
```
- Example: `bharatanatyam_v001.mp4`, `hip_hop_v042.mp4`
- `NNN` = zero-padded 3-digit video number (001–999)

### Processed Videos (resized, normalized, trimmed)
```
{dance_type}_v{NNN}_proc.mp4
```
- Example: `bhangra_v012_proc.mp4`

---

## Frames (JPEG images extracted per video)

```
{dance_type}_v{NNN}_f{FFFF}.jpg
```
- Example: `kathak_v005_f0001.jpg`, `salsa_v018_f0120.jpg`
- `FFFF` = zero-padded 4-digit frame number (0001–9999)

All frames for a video go into:
```
extracted_frames/{category}/{dance_type}/{dance_type}_v{NNN}/
```

---

## Pose Keypoints (.npy arrays)

### Per-sequence keypoint array  (shape: [30, 33, 4])
```
{dance_type}_v{NNN}_seq{SSS}.npy
```
- Example: `ballet_v007_seq001.npy`
- Array shape: `[sequence_length, 33_landmarks, 4_coords]`
- Coords order: `[x, y, z, visibility]`

### Per-frame keypoint file  (shape: [33, 4])
```
{dance_type}_v{NNN}_f{FFFF}_kp.npy
```
- Example: `breakdance_v003_f0045_kp.npy`

---

## Annotations (JSON)

### Per-video annotation
```
{dance_type}_v{NNN}_annotation.json
```
- Example: `tango_v011_annotation.json`

---

## Sample Sequences

### Training-ready sequence files
```
{dance_type}_seq_{SPLIT}_{INDEX}.npy
```
- Example: `garba_seq_train_00001.npy`
- `SPLIT` = `train` | `val` | `test`
- `INDEX` = zero-padded 5-digit index

---

## Dataset Split Manifest Files

Located in `dataset/splits/`:

```
train_manifest.csv
val_manifest.csv
test_manifest.csv
```

Each manifest contains:
```
sequence_file,label_id,dance_type,category,video_id,split
```

---

## Category Folder Names

| Category Display Name    | Folder Name           |
|--------------------------|-----------------------|
| Indian Classical         | indian_classical      |
| Indian Folk              | indian_folk           |
| Western Street           | western_street        |
| Contemporary / Modern    | contemporary_modern   |
| Latin / Ballroom         | latin_ballroom        |
| Commercial / Social      | commercial_social     |

---

## Dance Type Folder Names

| Display Name    | Folder Name    |
|-----------------|----------------|
| Hip-Hop         | hip_hop        |
| Breakdance      | breakdance     |
| K-Pop           | k_pop          |
| Cha-Cha         | cha_cha        |
| All others      | lowercase name |

---

## Rules Summary

1. All names are **lowercase with underscores** — no spaces, no hyphens.
2. Numeric indices are **zero-padded** to fixed width.
3. Video IDs use the format `{dance_type}_v{NNN}`.
4. Sequence IDs append `_seq{SSS}` to the video ID.
5. Frame IDs append `_f{FFFF}` to the video ID.
6. Never mix category or dance names across directories.
