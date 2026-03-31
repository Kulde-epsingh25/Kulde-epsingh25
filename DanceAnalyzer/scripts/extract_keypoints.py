"""
Dance Analyzer — Keypoint Extractor  v2
========================================
Multi-backend pose keypoint extractor that streams frames from videos or
image directories and saves .npy sequence arrays ready for model training.

Backends
--------
  mediapipe  — MediaPipe BlazePose body-only       output: [seq_len, 33, 4]
                 (x, y, z, visibility)
  holistic   — MediaPipe Holistic: body + hands    output: [seq_len, 75, 4]
                 body(33) + left_hand(21) + right_hand(21)
                 *** RECOMMENDED for Indian Classical dance (mudras) ***
  movenet    — TF Hub MoveNet (Lightning or Thunder) output: [seq_len, 17, 3]
                 (x, y, score) — 17 COCO keypoints, GPU-friendly

Installation
------------
  pip install mediapipe opencv-python numpy tqdm           # mediapipe / holistic
  pip install tensorflow tensorflow-hub                    # movenet

Usage
-----
  # Indian Classical: full body + both hands (mudras)
  python scripts/extract_keypoints.py \\
      --video-dir dataset/videos/indian_classical/bharatanatyam/raw_videos \\
      --output-dir dataset/pose_keypoints/indian_classical/bharatanatyam \\
      --label-id 0 --backend holistic

  # Fast MoveNet Thunder extraction
  python scripts/extract_keypoints.py \\
      --video-dir dataset/videos/indian_classical/kathak/raw_videos \\
      --output-dir dataset/pose_keypoints/indian_classical/kathak \\
      --label-id 1 --backend movenet --movenet-variant thunder

  # From still images
  python scripts/extract_keypoints.py \\
      --image-dir dataset/raw_images/indian_classical/bharatanatyam \\
      --output-dir dataset/pose_keypoints/indian_classical/bharatanatyam \\
      --label-id 0 --backend holistic
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
    # Fallback: no-op wrapper that matches tqdm's interface
    class tqdm:  # type: ignore[no-redef]
        def __init__(self, iterable=None, **kwargs):
            self._iterable = iterable

        def __iter__(self):
            return iter(self._iterable) if self._iterable is not None else iter([])

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def update(self, n=1):
            pass

        @staticmethod
        def write(msg, **kwargs):
            print(msg)

        def set_postfix(self, **kwargs):
            pass


# ─── Landmark counts ──────────────────────────────────────────────────────────
_MP_BODY_N = 33     # BlazePose body
_MP_HAND_N = 21     # MediaPipe hand
_MN_KP_N   = 17     # MoveNet COCO keypoints

# MoveNet Thunder input size (pixels)
_MOVENET_THUNDER_SIZE = 256
_MOVENET_LIGHTNING_SIZE = 192


# ─── Backend classes ──────────────────────────────────────────────────────────

class MediaPipeBackend:
    """BlazePose body-only backend — output shape: [33, 4]."""

    def __init__(self) -> None:
        try:
            import mediapipe as mp
        except ImportError:
            raise SystemExit("mediapipe is required: pip install mediapipe")
        self._pose = mp.solutions.pose.Pose(
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.6,
        )

    def process_frame(self, rgb: np.ndarray) -> np.ndarray:
        """Return [33, 4] array (x, y, z, visibility)."""
        results = self._pose.process(rgb)
        if results.pose_landmarks:
            return np.array(
                [[lm.x, lm.y, lm.z, lm.visibility]
                 for lm in results.pose_landmarks.landmark],
                dtype=np.float32,
            )
        return np.zeros((_MP_BODY_N, 4), dtype=np.float32)

    def mean_confidence(self, kp: np.ndarray) -> float:
        """Mean visibility score (channel index 3)."""
        return float(kp[:, 3].mean())

    def close(self) -> None:
        self._pose.close()

    @property
    def name(self) -> str:
        return "mediapipe"


class HolisticBackend:
    """MediaPipe Holistic: body + left hand + right hand — output shape: [75, 4].

    Index layout
    ------------
    0 – 32  : BlazePose body (x, y, z, visibility)
    33 – 53 : Left hand (x, y, z, 1.0 if detected else 0.0)
    54 – 74 : Right hand (x, y, z, 1.0 if detected else 0.0)

    Best choice for Indian Classical dance because it captures mudras
    (hand gestures) that carry semantic meaning in Bharatanatyam, Kathak, etc.
    """

    def __init__(self) -> None:
        try:
            import mediapipe as mp
        except ImportError:
            raise SystemExit("mediapipe is required: pip install mediapipe")
        self._holistic = mp.solutions.holistic.Holistic(
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.6,
        )

    def process_frame(self, rgb: np.ndarray) -> np.ndarray:
        """Return [75, 4] array: body(33) + left_hand(21) + right_hand(21)."""
        results = self._holistic.process(rgb)

        # Body pose: [33, 4]
        if results.pose_landmarks:
            body = np.array(
                [[lm.x, lm.y, lm.z, lm.visibility]
                 for lm in results.pose_landmarks.landmark],
                dtype=np.float32,
            )
        else:
            body = np.zeros((_MP_BODY_N, 4), dtype=np.float32)

        # Left hand: [21, 4]  (visibility = 1.0 if landmarks present)
        if results.left_hand_landmarks:
            lh = np.array(
                [[lm.x, lm.y, lm.z, 1.0]
                 for lm in results.left_hand_landmarks.landmark],
                dtype=np.float32,
            )
        else:
            lh = np.zeros((_MP_HAND_N, 4), dtype=np.float32)

        # Right hand: [21, 4]
        if results.right_hand_landmarks:
            rh = np.array(
                [[lm.x, lm.y, lm.z, 1.0]
                 for lm in results.right_hand_landmarks.landmark],
                dtype=np.float32,
            )
        else:
            rh = np.zeros((_MP_HAND_N, 4), dtype=np.float32)

        return np.concatenate([body, lh, rh], axis=0)  # [75, 4]

    def mean_confidence(self, kp: np.ndarray) -> float:
        """Mean visibility/confidence across all 75 landmarks."""
        return float(kp[:, 3].mean())

    def close(self) -> None:
        self._holistic.close()

    @property
    def name(self) -> str:
        return "holistic"


class MoveNetBackend:
    """TF Hub MoveNet backend — output shape: [17, 3].

    Keypoint order (COCO 17): nose, left_eye, right_eye, left_ear, right_ear,
    left_shoulder, right_shoulder, left_elbow, right_elbow, left_wrist,
    right_wrist, left_hip, right_hip, left_knee, right_knee, left_ankle,
    right_ankle.

    Output coords are (x, y, score) — normalised 0-1 relative to frame size.
    """

    _THUNDER_URL  = "https://tfhub.dev/google/movenet/singlepose/thunder/4"
    _LIGHTNING_URL = "https://tfhub.dev/google/movenet/singlepose/lightning/4"

    def __init__(self, variant: str = "thunder") -> None:
        try:
            import tensorflow as tf
            import tensorflow_hub as hub
        except ImportError:
            raise SystemExit(
                "TensorFlow and tensorflow-hub are required for MoveNet:\n"
                "  pip install tensorflow tensorflow-hub"
            )
        url = self._THUNDER_URL if variant == "thunder" else self._LIGHTNING_URL
        self._input_size = (
            _MOVENET_THUNDER_SIZE if variant == "thunder" else _MOVENET_LIGHTNING_SIZE
        )
        module = hub.load(url)
        self._infer = module.signatures["serving_default"]
        self._tf = tf
        print(f"  MoveNet {variant} loaded from TF Hub.")

    def process_frame(self, rgb: np.ndarray) -> np.ndarray:
        """Return [17, 3] array (x, y, score)."""
        tf = self._tf
        img = tf.image.resize_with_pad(
            tf.expand_dims(tf.cast(rgb, tf.int32), 0),
            self._input_size,
            self._input_size,
        )
        outputs = self._infer(tf.cast(img, tf.int32))
        kps = outputs["output_0"].numpy()[0, 0]  # [17, 3] as (y, x, score)
        # Swap y, x → x, y so output is (x, y, score) consistently
        result = kps.copy()
        result[:, 0] = kps[:, 1]
        result[:, 1] = kps[:, 0]
        return result.astype(np.float32)

    def mean_confidence(self, kp: np.ndarray) -> float:
        """Mean score (channel index 2)."""
        return float(kp[:, 2].mean())

    def close(self) -> None:
        pass  # No explicit cleanup needed for TF Hub modules

    @property
    def name(self) -> str:
        return "movenet"


def _build_backend(name: str, movenet_variant: str = "thunder"):
    """Factory: return the requested backend instance."""
    name = name.lower()
    if name == "mediapipe":
        return MediaPipeBackend()
    if name == "holistic":
        return HolisticBackend()
    if name == "movenet":
        return MoveNetBackend(variant=movenet_variant)
    raise ValueError(f"Unknown backend '{name}'. Choose: mediapipe | holistic | movenet")


# ─── Sequence builders ────────────────────────────────────────────────────────

def _frames_to_sequences(
    frames_kp: list[np.ndarray],
    backend,
    sequence_length: int,
    overlap: int,
    min_confidence: float,
) -> list[np.ndarray]:
    """Slide a window over frame keypoints and return valid sequences."""
    step = sequence_length - overlap
    sequences = []
    for start in range(0, len(frames_kp) - sequence_length + 1, step):
        seq = np.array(frames_kp[start: start + sequence_length], dtype=np.float32)
        conf = float(np.mean([backend.mean_confidence(f) for f in frames_kp[start: start + sequence_length]]))
        if conf >= min_confidence:
            sequences.append(seq)
    return sequences


def video_to_sequences(
    video_path: str,
    backend,
    sequence_length: int = 30,
    overlap: int = 10,
    min_confidence: float = 0.5,
) -> list[np.ndarray]:
    """Stream a video file and return qualifying keypoint sequences."""
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames_kp: list[np.ndarray] = []

    with tqdm(total=total_frames, desc=os.path.basename(video_path),
              unit="fr", leave=False) as pbar:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames_kp.append(backend.process_frame(rgb))
            pbar.update(1)

    cap.release()
    return _frames_to_sequences(frames_kp, backend, sequence_length, overlap, min_confidence)


def images_to_sequences(
    image_dir: str,
    backend,
    sequence_length: int = 30,
    overlap: int = 10,
    min_confidence: float = 0.5,
) -> list[np.ndarray]:
    """Load ordered images from a directory and return qualifying sequences."""
    image_files = sorted(
        f for f in os.listdir(image_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".webp"))
    )
    frames_kp: list[np.ndarray] = []

    for image_file in tqdm(image_files, desc=os.path.basename(image_dir), unit="img", leave=False):
        frame = cv2.imread(os.path.join(image_dir, image_file))
        if frame is None:
            continue
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames_kp.append(backend.process_frame(rgb))

    return _frames_to_sequences(frames_kp, backend, sequence_length, overlap, min_confidence)


# ─── Directory processor ──────────────────────────────────────────────────────

def process_directory(
    video_dir: str | None,
    image_dir: str | None,
    output_dir: str,
    label_id: int,
    sequence_length: int,
    overlap: int,
    backend_name: str,
    movenet_variant: str,
    min_confidence: float,
) -> None:
    os.makedirs(output_dir, exist_ok=True)
    backend = _build_backend(backend_name, movenet_variant)
    print(f"  Backend : {backend.name}  |  seq_len={sequence_length}  overlap={overlap}  min_conf={min_confidence}")

    total_seqs = 0
    try:
        if video_dir:
            video_files = sorted(
                f for f in os.listdir(video_dir)
                if f.lower().endswith((".mp4", ".avi", ".mov", ".mkv", ".webm"))
            )
            if not video_files:
                print(f"  ⚠️  No video files found in {video_dir}")
            for vid_file in tqdm(video_files, desc="Videos", unit="vid"):
                video_path = os.path.join(video_dir, vid_file)
                stem = os.path.splitext(vid_file)[0]
                sequences = video_to_sequences(
                    video_path, backend, sequence_length, overlap, min_confidence
                )
                for idx, seq in enumerate(sequences, start=1):
                    out_path = os.path.join(output_dir, f"{stem}_seq{idx:03d}.npy")
                    np.save(out_path, seq)
                    total_seqs += 1
                tqdm.write(f"  {vid_file}: {len(sequences)} sequences")
        else:
            source_name = os.path.basename(os.path.normpath(image_dir)) or "raw_images"
            sequences = images_to_sequences(
                image_dir, backend, sequence_length, overlap, min_confidence
            )
            for idx, seq in enumerate(sequences, start=1):
                out_path = os.path.join(output_dir, f"{source_name}_seq{idx:03d}.npy")
                np.save(out_path, seq)
                total_seqs += 1
            print(f"  {image_dir}: {len(sequences)} sequences")
    finally:
        backend.close()

    print(f"\n✅  {total_seqs} sequences extracted → {output_dir}")
    if total_seqs:
        sample = np.load(os.path.join(output_dir, os.listdir(output_dir)[0]))
        print(f"    Shape per sequence: {sample.shape}")


# ─── Entry point ──────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract pose keypoints from dance videos or images.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Backends:
  mediapipe  → [seq_len, 33, 4]  BlazePose body (x, y, z, visibility)
  holistic   → [seq_len, 75, 4]  Body + both hands (BEST for Indian Classical)
  movenet    → [seq_len, 17, 3]  MoveNet 17 COCO keypoints (x, y, score)
        """,
    )
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--video-dir", help="Directory containing raw video files")
    src.add_argument("--image-dir", help="Directory containing ordered still images")

    parser.add_argument("--output-dir", required=True,
                        help="Directory to save .npy keypoint sequences")
    parser.add_argument("--label-id", type=int, required=True,
                        help="Integer class label (see dataset/metadata/labels.json)")
    parser.add_argument("--backend", default="holistic",
                        choices=["mediapipe", "holistic", "movenet"],
                        help="Pose estimation backend (default: holistic)")
    parser.add_argument("--movenet-variant", default="thunder",
                        choices=["lightning", "thunder"],
                        help="MoveNet variant — thunder is more accurate (default: thunder)")
    parser.add_argument("--sequence-length", type=int, default=30,
                        help="Frames per sequence (default: 30)")
    parser.add_argument("--overlap", type=int, default=10,
                        help="Overlapping frames between adjacent sequences (default: 10)")
    parser.add_argument("--min-confidence", type=float, default=0.5,
                        help="Minimum mean landmark confidence to keep a sequence (default: 0.5)")
    args = parser.parse_args()

    process_directory(
        video_dir=args.video_dir,
        image_dir=args.image_dir,
        output_dir=args.output_dir,
        label_id=args.label_id,
        sequence_length=args.sequence_length,
        overlap=args.overlap,
        backend_name=args.backend,
        movenet_variant=args.movenet_variant,
        min_confidence=args.min_confidence,
    )


if __name__ == "__main__":
    main()
