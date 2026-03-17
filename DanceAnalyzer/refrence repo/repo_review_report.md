# Reference Repository Review for DanceAnalyzer

Date: 2026-03-17
Scope: Review 9 external dance ML repositories, identify what is reusable for DanceAnalyzer (39-class dance recognition with MediaPipe pose sequences), and mark low-value parts.

## Executive Summary

Best immediate reuse candidates:
1. DanceVision-AI-Driven-Dance-Proficiency-Assessment
2. LabanCompiler
3. Transpondancer (limited reuse)

Mostly not useful for current scope (dataset + recognition/classification):
1. Music-Dance-Video-Synthesis (video generation task)
2. Deep-Dance (single-video generation experiment)
3. Deep-Learning-Framework-for-Aesthetic-and-Biomechanical-Optimization-of-Dance-Movements (different objective)
4. Oh-Dance-AI (Teachable Machine image-level approach)
5. dance-deep-learning-resources (resource list only)

## Repo-by-Repo Assessment

### 1) DanceVision-AI-Driven-Dance-Proficiency-Assessment
URL: https://github.com/zin288/DanceVision-AI-Driven-Dance-Proficiency-Assessment

What it does:
- Uses MediaPipe pose landmarks and classical ML for pose-level proficiency checks.
- Extracts selected landmarks and trains sklearn classifiers.

Potentially useful for DanceAnalyzer:
- Landmark extraction pipeline patterns and video loop setup.
- Quick baseline classifier scripts for sanity checks before deep models.
- Demo overlay ideas for future inference visualization.

Concrete files:
- 01_training_data.py: frame loop + MediaPipe extraction + CSV writing.
- 02_pose_model_training.py: sklearn model benchmarking pattern.
- 03_pose_predictions_demo.py: prediction overlay and confidence display.

What is low value / not aligned:
- Built around key-pose binary/multi-pose proficiency feedback, not 39-class sequence recognition.
- Uses only 12 landmarks with x,y (no z/visibility), reducing signal compared with your [30,33,4] design.
- Small choreography-specific setup.

Verdict:
- Reuse selected utility ideas, not the end-to-end training strategy.

---

### 2) Music-Dance-Video-Synthesis
URL: https://github.com/xrenaa/Music-Dance-Video-Synthesis

What it does:
- Self-supervised music-conditioned dance video synthesis (generation), not classification.

Potentially useful for DanceAnalyzer:
- Sequence modeling architecture references (GRU/GCN modules) for future research.
- Data organization examples for dance sequence pipelines.

What is low value / not aligned:
- Core target is generation from music, not dance-type recognition.
- Old stack (python 3.5, pytorch 1.0) and heavy dependencies.
- Training/evaluation goals are different from your manifests + label_id classification objective.

Verdict:
- Keep as research reference only. Do not integrate into v1 pipeline.

---

### 3) Transpondancer
URL: https://github.com/Yuning-J/Transpondancer

What it does:
- Image/frame based movement classification and text annotation concepts.

Potentially useful for DanceAnalyzer:
- Dataset loader/normalization patterns for variable image sizes.
- Class-folder conventions in data handlers.
- Baseline CNN training structure for frame-level experiments.

Concrete file:
- src/Ballet/datahandler.py: robust image preprocessing/collation ideas.

What is low value / not aligned:
- Primarily frame/image classification, not temporal pose sequence modeling.
- Focused on small custom datasets (Ballet/Locking prototypes).
- Not designed around MediaPipe [x,y,z,visibility] sequence tensors.

Verdict:
- Reuse preprocessing concepts only if you build frame-baselines; otherwise low priority.

---

### 4) dance-deep-learning-resources
URL: https://github.com/dancelogue/dance-deep-learning-resources

What it does:
- Curated links to papers, blogs, external tools.

Potentially useful for DanceAnalyzer:
- Literature discovery list.

What is low value / not aligned:
- No runnable pipeline/code to integrate.

Verdict:
- Useful as bibliography, not implementation source.

---

### 5) LabanCompiler
URL: https://github.com/koke1997/LabanCompiler

What it does:
- Video-to-Labanotation tool with MediaPipe Holistic components.

Potentially useful for DanceAnalyzer:
- Modular microservice structure around video input and pose estimation.
- Holistic landmark extraction functions (pose + hands + face) for future multimodal expansion.
- Webcam/visual debug utilities.

Concrete file:
- microservices/pose_estimation/perform_pose_estimation.py: reusable pattern for batched frame processing with MediaPipe.

What is low value / not aligned:
- Main output is notation conversion, not class recognition.
- Includes extra modalities (hands/face) that increase complexity and storage.

Verdict:
- Good engineering reference for modular extraction service design. Medium reuse.

---

### 6) Oh-Dance-AI
URL: https://github.com/reevald/Oh-Dance-AI

What it does:
- Traditional dance movement classification with Teachable Machine + an NLP recommendation component.

Potentially useful for DanceAnalyzer:
- Product ideas (educational UI, recommendation/search module) for a future app layer.

What is low value / not aligned:
- CV model is external Teachable Machine workflow; model artifacts not fully in repo.
- Very small image datasets and acknowledged bias.
- Not sequence-based pose tensor pipeline.

Verdict:
- Low technical reuse for core ML pipeline; maybe useful for downstream app UX ideas.

---

### 7) Deep-Dance
URL: https://github.com/akashraj9828/Deep-Dance

What it does:
- Autoencoder + RNN pipeline to generate dance-like video frames from a single source video.

Potentially useful for DanceAnalyzer:
- Minimal experimentation reference for temporal generation.

What is low value / not aligned:
- Generation objective, not dance classification.
- Single-video experimental setup, heavy preprocessing assumptions.
- No class-balanced multi-dance recognition methodology.

Verdict:
- Not useful for current project scope.

---

### 8) Deep-Learning-Framework-for-Aesthetic-and-Biomechanical-Optimization-of-Dance-Movements
URL: https://github.com/YingShen2091/Deep-Learning-Framework-for-Aesthetic-and-Biomechanical-Optimization-of-Dance-Movements

What it does:
- Predicts aesthetic/biomechanical quality and optimizes movement via RL.

Potentially useful for DanceAnalyzer:
- Possible future extension after classification (scoring quality).
- Configuration-driven project structure is a decent template.

What is low value / not aligned:
- Different target labels (scores/optimization) vs dance-type classification labels.
- Increased model and compute complexity without helping initial dataset pipeline.

Verdict:
- Out of scope for v1; consider only after classifier baseline is stable.

---

### 9) AI-Dance-based-on-Human-Pose-Estimation
URL: https://github.com/Devashi-Choudhary/AI-Dance-based-on-Human-Pose-Estimation

What it does:
- OpenPose-style skeleton extraction and LSTM mapping from audio tempogram to pose output.

Potentially useful for DanceAnalyzer:
- Missing-value imputation idea for noisy keypoint streams.
- Skeleton sequence handling patterns.

Concrete files:
- src/main.py: sequence preprocessing and imputation logic.
- src/extract_data.py: data collection script.

What is low value / not aligned:
- Primary objective is audio-to-motion generation, not dance-type recognition.
- Uses YouTube download flow; should not be used directly in your pipeline.
- Legacy/rigid assumptions and hardcoded paths in parts of the script.

Verdict:
- Reuse only the data-cleaning/imputation concepts.

## Final Usefulness Matrix

High value for immediate adaptation:
- DanceVision-AI-Driven-Dance-Proficiency-Assessment (selected parts)

Medium value:
- LabanCompiler
- Transpondancer
- AI-Dance-based-on-Human-Pose-Estimation (partial)

Low value for current scope:
- Music-Dance-Video-Synthesis
- Deep-Dance
- Deep-Learning-Framework-for-Aesthetic-and-Biomechanical-Optimization-of-Dance-Movements
- Oh-Dance-AI
- dance-deep-learning-resources

## Recommended Next Steps for DanceAnalyzer

1. Integrate quality filtering before sequence export:
- Landmark visibility thresholding per frame.
- Sequence accept/reject score for 30-frame windows.

2. Add a baseline classical ML benchmark script:
- Flatten selected landmarks from each sequence and run sklearn baseline.
- Use as quick sanity metric before deep temporal models.

3. Keep current project objective strict:
- Dance type classification first.
- Defer generation, Labanotation, RL optimization, and NLP recommendation to future phases.

4. Build a small reusable module in scripts:
- quality_filter.py (visibility checks + missing landmark ratio)
- baseline_classical_ml.py (quick baseline from train_manifest.csv)

---

Prepared for: DanceAnalyzer reference review
Location: DanceAnalyzer/refrence repo/repo_review_report.md
