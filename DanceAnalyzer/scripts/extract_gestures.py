"""
Dance Analyzer — Long-Video Gesture Extractor
==============================================
Designed for long performance recordings (10 min – several hours).

Pipeline
--------
  1. Fast motion analysis  — decode video at 1/4 resolution, compute per-frame
                             motion score (frame-difference mean).
  2. Scene detection       — split on large motion spikes (shot boundaries).
  3. Active-window finding — find contiguous high-motion segments, merge nearby
                             gaps, discard short static passages.
  4. Pose extraction       — run the chosen backend only on active windows,
                             streaming full-resolution frames efficiently.
  5. Save .npy sequences   — same format as extract_keypoints.py so
                             build_splits.py works unchanged.

Backend shapes (same as extract_keypoints.py)
----------------------------------------------
  mediapipe  → [seq_len, 33, 4]   (x, y, z, visibility)
  holistic   → [seq_len, 75, 4]   body(33) + L-hand(21) + R-hand(21)
  movenet    → [seq_len, 17, 3]   (x, y, score)

Installation
------------
  pip install mediapipe opencv-python numpy tqdm scipy   # mediapipe / holistic
  pip install tensorflow tensorflow-hub                  # movenet

Usage
-----
  # Process one long video — holistic backend (recommended for Indian Classical)
  python scripts/extract_gestures.py \\
      --video dataset/videos/indian_classical/bharatanatyam/raw_videos/bharatanatyam_v001.mp4 \\
      --output-dir dataset/pose_keypoints/indian_classical/bharatanatyam \\
      --label-id 0 --backend holistic

  # Process all videos in a directory
  python scripts/extract_gestures.py \\
      --video-dir dataset/videos/indian_classical/kathak/raw_videos \\
      --output-dir dataset/pose_keypoints/indian_classical/kathak \\
      --label-id 1 --backend holistic --min-motion 0.025

  # MoveNet — fastest, GPU-friendly
  python scripts/extract_gestures.py \\
      --video dataset/videos/western_street/breakdance/raw_videos/breakdance_v001.mp4 \\
      --output-dir dataset/pose_keypoints/western_street/breakdance \\
      --label-id 17 --backend movenet --movenet-variant thunder
"""

from __future__ import annotations

import os
import argparse
import numpy as np

try:
    import cv2
except ImportError:
    raise SystemExit("opencv-python is required: pip install opencv-python")

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):  # type: ignore[misc]
        return iterable if iterable is not None else range(0)

try:
    from scipy.ndimage import uniform_filter1d as _smooth
    _HAS_SCIPY = True
except ImportError:
    _HAS_SCIPY = False

# Re-use backend classes from extract_keypoints (same package directory)
import sys
_SCRIPTS_DIR = os.path.dirname(__file__)
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)
from extract_keypoints import _build_backend, _frames_to_sequences  # noqa: E402


# ─── Motion analysis ──────────────────────────────────────────────────────────

def _smooth_scores(scores: np.ndarray, window: int) -> np.ndarray:
    """Apply a simple uniform moving average."""
    if _HAS_SCIPY:
        return _smooth(scores.astype(float), size=max(3, window))
    # Fallback: numpy-based rolling mean
    kernel = np.ones(max(3, window)) / max(3, window)
    return np.convolve(scores, kernel, mode="same")


def compute_motion_scores(video_path: str, scale: float = 0.25) -> tuple[np.ndarray, float]:
    """Compute per-frame motion score by comparing consecutive small frames.

    Parameters
    ----------
    video_path : str
        Path to the video file.
    scale : float
        Downscale factor used for fast motion analysis (default 0.25).

    Returns
    -------
    scores : np.ndarray  shape [N_frames]
        Per-frame normalised motion score in [0, 1].
    fps : float
        Video frames-per-second.
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    prev_gray: np.ndarray | None = None
    scores: list[float] = []

    with tqdm(total=total, desc="Motion analysis", unit="fr", leave=False) as pbar:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            h, w = frame.shape[:2]
            small = cv2.resize(frame, (max(1, int(w * scale)), max(1, int(h * scale))))
            gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

            if prev_gray is not None:
                diff = cv2.absdiff(gray, prev_gray)
                scores.append(float(diff.mean()) / 255.0)
            else:
                scores.append(0.0)

            prev_gray = gray
            pbar.update(1)

    cap.release()
    return np.array(scores, dtype=np.float32), float(fps)


# ─── Scene & active-window detection ─────────────────────────────────────────

def detect_scene_boundaries(scores: np.ndarray, fps: float,
                             scene_threshold: float = 0.15) -> list[int]:
    """Return frame indices where a hard cut / scene change is detected."""
    boundaries = [0]
    for i, s in enumerate(scores):
        if s > scene_threshold:
            boundaries.append(i)
    boundaries.append(len(scores))
    return boundaries


def find_active_windows(
    scores: np.ndarray,
    fps: float,
    min_motion: float = 0.03,
    min_duration_s: float = 1.0,
    merge_gap_s: float = 0.5,
) -> list[tuple[int, int]]:
    """Return a list of (start_frame, end_frame) active gesture windows.

    Parameters
    ----------
    scores : np.ndarray
        Per-frame motion scores from compute_motion_scores().
    fps : float
        Video FPS.
    min_motion : float
        Motion threshold — frames below this are considered static.
    min_duration_s : float
        Minimum window duration in seconds (discard shorter bursts).
    merge_gap_s : float
        Merge windows that are closer than this many seconds apart.
    """
    # Smooth over ~0.5 s to remove single-frame noise
    smooth_win = max(3, int(fps * 0.5))
    smoothed = _smooth_scores(scores, smooth_win)

    active = smoothed > min_motion
    min_frames = max(1, int(min_duration_s * fps))
    merge_gap = max(1, int(merge_gap_s * fps))

    # Find contiguous runs of active frames
    raw_windows: list[list[int]] = []
    in_window = False
    start = 0
    for i, a in enumerate(active):
        if a and not in_window:
            start = i
            in_window = True
        elif not a and in_window:
            if i - start >= min_frames:
                raw_windows.append([start, i])
            in_window = False
    if in_window and len(active) - start >= min_frames:
        raw_windows.append([start, len(active)])

    if not raw_windows:
        return []

    # Merge nearby windows
    merged: list[list[int]] = [raw_windows[0]]
    for w in raw_windows[1:]:
        if w[0] - merged[-1][1] <= merge_gap:
            merged[-1][1] = w[1]
        else:
            merged.append(w)

    return [(w[0], w[1]) for w in merged]


# ─── Pose extraction from windows ─────────────────────────────────────────────

def extract_window_sequences(
    video_path: str,
    windows: list[tuple[int, int]],
    backend,
    sequence_length: int,
    overlap: int,
    min_confidence: float,
) -> list[np.ndarray]:
    """Extract pose keypoint sequences only from active windows.

    Opens the video once and seeks to each window, avoiding redundant decoding
    of static/transition sections.
    """
    if not windows:
        return []

    cap = cv2.VideoCapture(video_path)
    all_sequences: list[np.ndarray] = []

    for win_start, win_end in tqdm(windows, desc="Windows", unit="win", leave=False):
        cap.set(cv2.CAP_PROP_POS_FRAMES, win_start)
        frames_kp: list[np.ndarray] = []
        frame_idx = win_start

        while frame_idx < win_end:
            ret, frame = cap.read()
            if not ret:
                break
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames_kp.append(backend.process_frame(rgb))
            frame_idx += 1

        seqs = _frames_to_sequences(
            frames_kp, backend, sequence_length, overlap, min_confidence
        )
        all_sequences.extend(seqs)

    cap.release()
    return all_sequences


# ─── Top-level video processor ───────────────────────────────────────────────

def process_video(
    video_path: str,
    output_dir: str,
    label_id: int,
    backend,
    sequence_length: int,
    overlap: int,
    min_motion: float,
    min_confidence: float,
    min_duration_s: float,
    merge_gap_s: float,
) -> int:
    """Full pipeline for one video. Returns number of sequences saved."""
    print(f"\n▶  {os.path.basename(video_path)}")

    # Step 1 — motion analysis
    scores, fps = compute_motion_scores(video_path)
    print(f"   Frames: {len(scores)}  FPS: {fps:.1f}  Motion mean: {scores.mean():.4f}")

    # Step 2 — find active windows
    windows = find_active_windows(
        scores, fps,
        min_motion=min_motion,
        min_duration_s=min_duration_s,
        merge_gap_s=merge_gap_s,
    )

    if not windows:
        print(f"   ⚠️  No active gesture windows found (try --min-motion {min_motion * 0.5:.4f})")
        return 0

    total_active_s = sum(e - s for s, e in windows) / fps
    print(f"   Active windows: {len(windows)}  ({total_active_s:.1f} s of {len(scores)/fps:.1f} s total)")

    # Step 3 — extract keypoints from active windows only
    sequences = extract_window_sequences(
        video_path, windows, backend, sequence_length, overlap, min_confidence
    )

    if not sequences:
        print("   ⚠️  No qualifying sequences after confidence filtering.")
        return 0

    # Step 4 — save
    stem = os.path.splitext(os.path.basename(video_path))[0]
    for idx, seq in enumerate(sequences, start=1):
        out_path = os.path.join(output_dir, f"{stem}_seq{idx:03d}.npy")
        np.save(out_path, seq)

    print(f"   ✅  Saved {len(sequences)} sequences  shape={sequences[0].shape}")
    return len(sequences)


# ─── Entry point ─────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract key gestures from long dance videos.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Motion thresholds (--min-motion):
  0.01 – very sensitive, picks up subtle finger movements
  0.03 – recommended default for Indian Classical (moderate movement)
  0.05 – high-motion styles (Breakdance, Bhangra)
  0.10 – only large, fast movements
        """,
    )
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--video", help="Path to a single video file")
    src.add_argument("--video-dir", help="Directory of video files to process in batch")

    parser.add_argument("--output-dir", required=True,
                        help="Directory to save .npy keypoint sequences")
    parser.add_argument("--label-id", type=int, required=True,
                        help="Integer class label")
    parser.add_argument("--backend", default="holistic",
                        choices=["mediapipe", "holistic", "movenet"],
                        help="Pose backend (default: holistic — best for Indian Classical)")
    parser.add_argument("--movenet-variant", default="thunder",
                        choices=["lightning", "thunder"],
                        help="MoveNet variant (default: thunder)")
    parser.add_argument("--sequence-length", type=int, default=30,
                        help="Frames per sequence (default: 30)")
    parser.add_argument("--overlap", type=int, default=10,
                        help="Overlapping frames between sequences (default: 10)")
    parser.add_argument("--min-motion", type=float, default=0.03,
                        help="Motion threshold — skip near-static frames (default: 0.03)")
    parser.add_argument("--min-confidence", type=float, default=0.5,
                        help="Minimum mean landmark confidence to keep a sequence (default: 0.5)")
    parser.add_argument("--min-duration", type=float, default=1.0,
                        help="Minimum active-window duration in seconds (default: 1.0)")
    parser.add_argument("--merge-gap", type=float, default=0.5,
                        help="Merge windows closer than this many seconds (default: 0.5)")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    backend = _build_backend(args.backend, args.movenet_variant)
    print(f"Backend: {backend.name}  |  seq_len={args.sequence_length}  "
          f"overlap={args.overlap}  min_conf={args.min_confidence}")

    video_files: list[str] = []
    if args.video:
        video_files = [args.video]
    else:
        video_files = sorted(
            os.path.join(args.video_dir, f)
            for f in os.listdir(args.video_dir)
            if f.lower().endswith((".mp4", ".avi", ".mov", ".mkv", ".webm"))
        )
        if not video_files:
            raise SystemExit(f"No video files found in {args.video_dir}")

    total_seqs = 0
    try:
        for vp in tqdm(video_files, desc="Processing videos", unit="vid",
                       disable=len(video_files) == 1):
            total_seqs += process_video(
                video_path=vp,
                output_dir=args.output_dir,
                label_id=args.label_id,
                backend=backend,
                sequence_length=args.sequence_length,
                overlap=args.overlap,
                min_motion=args.min_motion,
                min_confidence=args.min_confidence,
                min_duration_s=args.min_duration,
                merge_gap_s=args.merge_gap,
            )
    finally:
        backend.close()

    print(f"\n✅  Total sequences saved: {total_seqs}  →  {args.output_dir}")


if __name__ == "__main__":
    main()
