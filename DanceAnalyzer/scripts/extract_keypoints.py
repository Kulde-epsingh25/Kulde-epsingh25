"""
Dance Analyzer — Keypoint Extractor
=====================================
Extracts MediaPipe pose keypoints from video files and saves
them as .npy sequence arrays ready for model training.

Usage:
    python scripts/extract_keypoints.py \
        --video-dir dataset/videos/indian_classical/bharatanatyam/raw_videos \
        --output-dir dataset/pose_keypoints/indian_classical/bharatanatyam \
        --label-id 0 \
        --sequence-length 30 \
        --overlap 10

    # Optional: extract from still images
    python scripts/extract_keypoints.py \
        --image-dir dataset/raw_images/indian_classical/bharatanatyam \
        --output-dir dataset/pose_keypoints/indian_classical/bharatanatyam \
        --label-id 0 \
        --sequence-length 30 \
        --overlap 10
"""

import os
import argparse
import numpy as np

# MediaPipe is required: pip install mediapipe opencv-python
try:
    import cv2
    import mediapipe as mp
except ImportError:
    raise SystemExit(
        "Required packages missing. Install with:\n"
        "  pip install mediapipe opencv-python"
    )

NUM_LANDMARKS = 33   # BlazePose full-body
COORDS = 4           # x, y, z, visibility


def extract_keypoints_from_frame(results) -> np.ndarray:
    """Convert a MediaPipe pose result to a (33, 4) numpy array."""
    if results.pose_landmarks:
        return np.array(
            [
                [lm.x, lm.y, lm.z, lm.visibility]
                for lm in results.pose_landmarks.landmark
            ],
            dtype=np.float32,
        )
    return np.zeros((NUM_LANDMARKS, COORDS), dtype=np.float32)


def video_to_sequences(
    video_path: str,
    pose,
    sequence_length: int = 30,
    overlap: int = 10,
) -> list:
    """Return a list of (sequence_length, 33, 4) arrays from one video."""
    cap = cv2.VideoCapture(video_path)
    frames_kp = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)
        frames_kp.append(extract_keypoints_from_frame(results))

    cap.release()

    step = sequence_length - overlap
    sequences = []
    for start in range(0, len(frames_kp) - sequence_length + 1, step):
        seq = np.array(frames_kp[start : start + sequence_length], dtype=np.float32)
        sequences.append(seq)

    return sequences


def images_to_sequences(
    image_dir: str,
    pose,
    sequence_length: int = 30,
    overlap: int = 10,
) -> list:
    """Return a list of (sequence_length, 33, 4) arrays from ordered image files."""
    image_files = [
        f for f in os.listdir(image_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".webp"))
    ]

    frames_kp = []
    for image_file in sorted(image_files):
        image_path = os.path.join(image_dir, image_file)
        frame = cv2.imread(image_path)
        if frame is None:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)
        frames_kp.append(extract_keypoints_from_frame(results))

    step = sequence_length - overlap
    sequences = []
    for start in range(0, len(frames_kp) - sequence_length + 1, step):
        seq = np.array(frames_kp[start : start + sequence_length], dtype=np.float32)
        sequences.append(seq)

    return sequences


def process_directory(
    video_dir: str,
    image_dir: str,
    output_dir: str,
    label_id: int,
    sequence_length: int,
    overlap: int,
) -> None:
    os.makedirs(output_dir, exist_ok=True)

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        model_complexity=1,
        smooth_landmarks=True,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.6,
    )

    total_seqs = 0
    if video_dir:
        video_files = [
            f for f in os.listdir(video_dir)
            if f.lower().endswith((".mp4", ".avi", ".mov", ".mkv"))
        ]

        for vid_file in sorted(video_files):
            video_path = os.path.join(video_dir, vid_file)
            stem = os.path.splitext(vid_file)[0]
            sequences = video_to_sequences(video_path, pose, sequence_length, overlap)

            for idx, seq in enumerate(sequences, start=1):
                out_path = os.path.join(output_dir, f"{stem}_seq{idx:03d}.npy")
                np.save(out_path, seq)
                total_seqs += 1

            print(f"  {vid_file}: {len(sequences)} sequences saved")
    else:
        source_name = os.path.basename(os.path.normpath(image_dir)) or "raw_images"
        sequences = images_to_sequences(image_dir, pose, sequence_length, overlap)
        for idx, seq in enumerate(sequences, start=1):
            out_path = os.path.join(output_dir, f"{source_name}_seq{idx:03d}.npy")
            np.save(out_path, seq)
            total_seqs += 1

        print(f"  {image_dir}: {len(sequences)} sequences saved")

    pose.close()
    print(f"\n✅  {total_seqs} sequences extracted → {output_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract MediaPipe keypoints from dance videos.")
    parser.add_argument("--video-dir", required=False, help="Directory containing raw .mp4 videos")
    parser.add_argument("--image-dir", required=False, help="Directory containing ordered raw images")
    parser.add_argument("--output-dir", required=True, help="Directory to save .npy keypoint sequences")
    parser.add_argument("--label-id", type=int, required=True, help="Integer class label (see class_mapping.csv)")
    parser.add_argument("--sequence-length", type=int, default=30, help="Frames per sequence (default: 30)")
    parser.add_argument("--overlap", type=int, default=10, help="Overlapping frames between sequences (default: 10)")
    args = parser.parse_args()

    if bool(args.video_dir) == bool(args.image_dir):
        raise SystemExit("Provide exactly one source: --video-dir or --image-dir")

    process_directory(
        args.video_dir,
        args.image_dir,
        args.output_dir,
        args.label_id,
        args.sequence_length,
        args.overlap,
    )


if __name__ == "__main__":
    main()
