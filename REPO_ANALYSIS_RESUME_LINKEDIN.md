# Repository Analysis for Resume & LinkedIn

## 1) Portfolio Snapshot

This repository currently contains a mix of:
- **1 advanced ML/data-engineering project** (DanceAnalyzer)
- **8 vanilla JavaScript mini-projects** (UI + DOM + browser APIs)
- **2 React starter applications** (Create React App + Vite)

Overall profile positioning:
- **Frontend Developer (HTML/CSS/JS/React)**
- **Applied ML/Data Pipeline Builder (Computer Vision/Pose Estimation)**
- **Hands-on project builder with end-to-end foldering, scripting, and feature implementation**

---

## 2) Repository/Project Inventory

| Project | Type | Core Stack | Architecture Style | Working Condition |
|---|---|---|---|---|
| DanceAnalyzer | ML dataset + preprocessing pipeline | Python, NumPy, OpenCV, MediaPipe, TensorFlow Hub, MMPose | Script-based modular pipeline (`setup -> extract -> split`) with structured dataset layers | **Partially production-ready** (strong structure/docs; needs model training/inference app layer) |
| Calculator_V01 | Web mini app | HTML, CSS, JavaScript | Single-page DOM-driven calculator with custom expression parser | **Working** |
| Clocks/normal | Web mini app | HTML, CSS, JavaScript | Single-page real-time analog clock using interval updates | **Working** |
| Clocks/FibonacciClock | Visual animation mini app | HTML, CSS, JavaScript, SVG | SVG parametric golden-spiral rendering + CSS rotation animation | **Working** (visual demo, not full timekeeping clock) |
| ColorPalette | Web utility mini app | HTML, CSS, JavaScript | Single-page random palette generation + clipboard interactions | **Working** |
| Diary | Web app skeleton | HTML, CSS, JavaScript | Basic scaffold only | **Not implemented yet** |
| DragDrop | Web mini app | HTML, CSS, JavaScript | Kanban-style drag-and-drop board using native DnD API | **Working** |
| ExpenseTracker | Web mini app | HTML, CSS, JavaScript, localStorage | Form/event-driven transaction ledger with persistent browser storage | **Working** |
| Quizgame | Web mini app | HTML, CSS, JavaScript | Stateful quiz flow (start -> question loop -> result) | **Working** |
| React/01basicreact | React starter | React, CRA, Jest/RTL setup | Component-based SPA starter (`App` root) | **Working starter** |
| React/01vitereact | React starter | React, Vite, ESLint | Component-based SPA starter with modern Vite tooling | **Working starter** |

---

## 3) Detailed Analysis by Project

## A. DanceAnalyzer

### Purpose
Build a large-scale, pose-based dance recognition dataset pipeline covering **39 dance types** across **6 categories**.

### Technical Highlights
- Multi-backend pose extraction:
  - **MediaPipe BlazePose** (33 keypoints)
  - **MediaPipe Holistic** (75 keypoints, including hands)
  - **MoveNet** (17 keypoints, TF Hub)
  - **MMPose RTMPose** (up to 133 keypoints)
- Data pipeline scripts:
  - `setup_dataset.py` for taxonomy/folder bootstrapping
  - `extract_keypoints.py` for sequence generation (`.npy`)
  - `extract_gestures.py` for long-video active motion windows
  - `build_splits.py` for train/val/test manifests
- Strong metadata and naming conventions (`labels.json`, `dataset_info.json`, manifests)

### Architecture
- **Layered dataset architecture**:
  - `videos/` (raw + processed)
  - `extracted_frames/` / `raw_images/`
  - `pose_keypoints/`
  - `splits/` + manifest CSVs
  - `metadata/`
- **Pipeline architecture** with reusable backend abstraction and sequence generation.

### Resume/LinkedIn Keywords
`Computer Vision`, `Pose Estimation`, `MediaPipe`, `MMPose`, `MoveNet`, `Data Pipeline`, `Dataset Engineering`, `Video Processing`, `Feature Extraction`, `ML Preprocessing`, `Python`, `NumPy`, `OpenCV`.

### Working Condition
- Core data-engineering pipeline is well structured and documented.
- Project is ideal to present as **dataset/pipeline engineering work**.
- To position as full ML product, add model training/evaluation/inference UI.

---

## B. Frontend JavaScript Projects

### 1) Calculator_V01
- Implements custom arithmetic parsing with operator precedence and keyboard support.
- Good demonstration of event handling and input state management.
- **Keywords:** `JavaScript`, `DOM Manipulation`, `Event Handling`, `Expression Parsing`, `UI Logic`.

### 2) Clocks/normal
- Real-time analog clock with second/minute/hour hand transforms.
- **Keywords:** `JavaScript Timing`, `Date API`, `CSS Transforms`, `Real-time UI`.

### 3) Clocks/FibonacciClock
- SVG golden spiral generation using logarithmic spiral math.
- Strong visual/math-driven frontend example.
- **Keywords:** `SVG`, `Mathematical Visualization`, `Animation`, `Creative Coding`.

### 4) ColorPalette
- Random hex palette generation and clipboard copy interaction.
- **Keywords:** `UI Utilities`, `Clipboard API`, `Randomization`, `Interactive Design Tools`.

### 5) Diary
- Scaffold exists but functionality is not implemented.
- **Keywords:** `Project Scaffolding`, `UI Skeleton`.

### 6) DragDrop
- Kanban-style board with add-card flow and native drag/drop interactions.
- **Keywords:** `Drag and Drop API`, `Task Board`, `Interactive UI`, `State Handling`.

### 7) ExpenseTracker
- Tracks income/expenses with totals and localStorage persistence.
- **Keywords:** `CRUD-like UI`, `localStorage`, `Financial Tracker`, `Form Validation`.

### 8) Quizgame
- Multi-screen quiz flow, dynamic answer rendering, score tracking, progress bar.
- **Keywords:** `State Management`, `Dynamic Rendering`, `Gamification UI`, `User Feedback`.

### Working Condition (Frontend Set)
- Most projects are functional and suitable as **practice/demo projects**.
- `Diary` is currently incomplete and should be completed or hidden from portfolio listing.

---

## C. React Projects

### 1) 01basicreact (Create React App)
- Minimal React app, CRA toolchain, testing scaffolding included.
- **Keywords:** `React`, `Create React App`, `Component Architecture`, `Jest`, `React Testing Library`.

### 2) 01vitereact (Vite)
- Minimal React app with modern Vite build tool and ESLint.
- **Keywords:** `React`, `Vite`, `ESLint`, `Frontend Tooling`, `Modern Build Systems`.

### Working Condition (React Set)
- Both are starter-level repositories and should be framed as **foundation/tooling demos**, not full production apps.

---

## 4) Recommended Resume Positioning

## Strongest Resume Feature
- **DanceAnalyzer** should be your flagship project.

## Suggested Positioning Statement
- “Built a modular computer-vision dataset pipeline for dance recognition across 39 classes using MediaPipe/MoveNet/MMPose, including automated sequence extraction, metadata management, and train/validation/test split generation.”

## Supporting Portfolio Layer
- Add 2–3 best frontend projects under “Interactive Web Apps”:
  - ExpenseTracker
  - DragDrop
  - Quizgame (or Calculator)

## Projects to Improve Before Highlighting
- Diary (finish implementation)
- React starters (expand into real apps with routing/API/state patterns)

---

## 5) Recruiter/Search Keywords Bank

Use these across resume, LinkedIn headline/about, and project descriptions:

- `Software Developer`
- `Frontend Developer`
- `JavaScript Developer`
- `React Developer`
- `HTML CSS JavaScript`
- `Computer Vision`
- `Machine Learning Pipeline`
- `Pose Estimation`
- `Data Preprocessing`
- `OpenCV`
- `MediaPipe`
- `MMPose`
- `Dataset Engineering`
- `Python Developer`
- `Problem Solving`
- `Project-Based Learning`

---

## 6) Final Portfolio Readiness Status

- **Ready to showcase now:** DanceAnalyzer, ExpenseTracker, DragDrop, Quizgame, Calculator, ColorPalette, Normal Clock
- **Show as creative demo:** FibonacciClock
- **Show as starter/foundation only:** React/01basicreact, React/01vitereact
- **Not ready yet:** Diary

