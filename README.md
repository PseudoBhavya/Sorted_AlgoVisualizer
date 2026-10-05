# 🧠 Sorted — "Look Inside the Algorithm"

<p align="center">
  <img src="brain.png" alt="Sorted Logo" width="96" height="96" />
</p>

<p align="center">
  <strong>Advanced Interactive Algorithm Execution, Visualization, and Empirical Analysis Platform</strong><br>
  <em>Sorted IDE v3.12 • End-Semester Capstone Project • BCA Advanced Python Curriculum</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/PyQt6-41CD52?style=for-the-badge&logo=qt&logoColor=white" alt="PyQt6" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas" />
  <img src="https://img.shields.io/badge/Tests-16%20Passed-10B981?style=for-the-badge&logo=checkmarx&logoColor=white" alt="Tests Passed" />
</p>

---

## 🌟 Overview

**Sorted** is an interactive computer science workbench engineered to demystify complex data structures and algorithmic mechanics. Unlike traditional visualizers that replay canned animations or static CSS transitions, Sorted is powered by a **Pure Python Execution Trace Engine** that records every genuine runtime computational event:
- Pointer movements ($i, j, \text{low}, \text{mid}, \text{high}$)
- Active element comparisons and condition checks
- In-memory swaps and array mutations with visual curved arcs
- Dynamic Programming state matrix updates
- Graph edge relaxations and heuristic cost recalculations ($g(n), h(n), f(n)$)
- Recursive call stack frames and boundary scopes

Designed in an obsidian-slate developer dark mode inspired by modern IDEs, Sorted pairs visual intuition with synchronized Python source code tracking, variable watches, and real-time auditory synthesis.

---

## ✨ Key Features

- **11 Core Algorithms Implemented**: Covering sorting, searching, graph traversal, and dynamic programming.
- **Synchronized Source Code Tracker**: Live line-by-line syntax-highlighted Python code view that updates simultaneously as each algorithm step executes.
- **Pedagogical Invariant Card ("Why this step?")**: Dynamic explanation detailing the rationale, computational invariant, and state changes occurring at every cycle.
- **Full-Width Interactive Control Bar**:
  - Scrubbing timeline progress slider
  - Play / Pause / Step Forward / Step Backward
  - Variable playback speed control (0.25x to 4x)
  - Web Audio tone synthesizer toggle
- **Auditory Cues (Web Audio API)**: Sound frequencies mapped to element values and state operations (higher pitch for larger elements, distinct tones for comparisons, swaps, and path finding).
- **Multi-Tab Telemetry & Visualizations**:
  - **Simulation Canvas**: Dynamic height-scaled array bars, SVG swap curves, interactive SVG graph network, 2D grid maze, and DP table.
  - **Matrix 2D View**: Grid representation of arrays and cost matrices.
  - **Bitfield / Binary Memory View**: Low-level representation of data states.
  - **Call Stack & Recursion Tree**: Real-time stack frame visualization for recursive algorithms.
- **Comparison & Benchmark Arena**: Run algorithms head-to-head on identical datasets and analyze runtime, comparisons, swaps, and memory overhead via Pandas DataFrames.
- **Dataset Generation & File I/O**: Generate uniform, nearly sorted, reversed, or few-unique distributions, or import/export via CSV, JSON, XML, and TXT.
- **Tri-Platform Architecture**:
  1. **Web IDE**: Streamlit-hosted responsive web application (`app.py`).
  2. **REST API**: Flask backend providing JSON execution traces (`run_api.py`).
  3. **Desktop App**: Native PyQt6 GUI with custom QPainter graphics (`run_gui.py`).

---

## 📚 Supported Algorithms & Complexity Matrix

| Algorithm | Category | Best Time | Average Time | Worst Time | Space Complexity | Stability |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Quick Sort (Hoare & Lomuto)** | Sorting | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(\log n)$ | Unstable |
| **Merge Sort** | Sorting | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n)$ | Stable |
| **Heap Sort** | Sorting | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(1)$ | Unstable |
| **Insertion Sort** | Sorting | $\mathcal{O}(n)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(1)$ | Stable |
| **Selection Sort** | Sorting | $\mathcal{O}(n^2)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(1)$ | Unstable |
| **Bubble Sort** | Sorting | $\mathcal{O}(n)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(1)$ | Stable |
| **Binary Search** | Searching | $\mathcal{O}(1)$ | $\mathcal{O}(\log n)$ | $\mathcal{O}(\log n)$ | $\mathcal{O}(1)$ | — |
| **Linear Search** | Searching | $\mathcal{O}(1)$ | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | — |
| **Dijkstra's Algorithm** | Graph / Pathfinding | $\mathcal{O}((V + E) \log V)$ | $\mathcal{O}((V + E) \log V)$ | $\mathcal{O}(V^2)$ | $\mathcal{O}(V)$ | — |
| **A\* Pathfinding** | Graph / Heuristic | $\mathcal{O}(E)$ | $\mathcal{O}(b^d)$ | $\mathcal{O}(b^d)$ | $\mathcal{O}(V)$ | — |
| **0/1 Knapsack Problem** | Dynamic Programming | $\mathcal{O}(n \cdot W)$ | $\mathcal{O}(n \cdot W)$ | $\mathcal{O}(n \cdot W)$ | $\mathcal{O}(n \cdot W)$ | — |

---

## 📐 Workspace Layout & Design Architecture

The primary workspace implements an ergonomic, data-dense IDE layout designed for focused learning:

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│  🧠 Sorted IDE    │  Sorting ▾  │  Searching ▾  │  Graph ▾  │  DP ▾  │ Arena │
├──────────────────────────────────────┬───────────────────────────────────────┤
│                                      │                                       │
│  [LEFT COLUMN: SIMULATION & CONFIG]  │  [RIGHT COLUMN: CODE & EXECUTION]     │
│                                      │                                       │
│  ┌────────────────────────────────┐  │  ┌─────────────────────────────────┐  │
│  │ Primary Visualizer Canvas      │  │  │ Python Source Tracker (Square)  │  │
│  │ (Bars / Graph SVG / Grid / DP) │  │  │ [Line-by-line real-time pointer]│  │
│  └────────────────────────────────┘  │  └─────────────────────────────────┘  │
│  ┌────────────────────────────────┐  │  ┌─────────────────────────────────┐  │
│  │ Configuration & Data Controls  │  │  │ Execution State & Variable Watch│  │
│  │ (Size, Speed, Dataset, Target) │  │  │ Pointers: i, j | Comparisons    │  │
│  └────────────────────────────────┘  │  └─────────────────────────────────┘  │
│  ┌────────────────────────────────┐  │  ┌─────────────────────────────────┐  │
│  │ Visual Tabs:                   │  │  │ Why this step? (Invariant Card) │  │
│  │ [Simulation][Matrix][Memory]   │  │  │ Explaining invariant condition  │  │
│  └────────────────────────────────┘  │  └─────────────────────────────────┘  │
├──────────────────────────────────────────────────────────────────────────────┤
│  [BOTTOM FULL-WIDTH TIMELINE CONTROLLER]                                     │
│  [◀◀ Step Back]  [▶ Play / ❚❚ Pause]  [Step Forward ▶▶]  [──●────── Scrubber]│
│  Speed: [1x ▾]  Audio Cues: [🔊 ON]  Progress: Step 14 of 48                 │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 🏛 Syllabus Mapping (BCA Advanced Python)

Sorted was architected to fulfill and exceed the requirements of the four-unit BCA curriculum:

| Unit | Subject Matter | Implementation in Sorted |
| :--- | :--- | :--- |
| **Unit 1** | **Advanced Object-Oriented Programming** | Abstract Base Classes (`abc.ABC`, `@abstractmethod`), class inheritance hierarchies, polymorphic dispatch, custom exception hierarchies (`AlgorithmError`, `InvalidInputError`, `EmptyDataError`). |
| **Unit 2** | **Algorithms & Computational Mechanics** | 11 algorithms across 4 paradigms with pure AST/event-driven `ExecutionTrace` capturing all state mutations, recursive call stack frames, and boundary checks. |
| **Unit 3** | **Web Engineering, Desktop GUI & Regex** | **Streamlit** Web Workbench (`app.py`), **PyQt6** Native Desktop GUI (`run_gui.py`), **Flask** REST API (`run_api.py`), and robust regex validation for custom user input (`algolens/validation/`). |
| **Unit 4** | **File Handling, Serialization & Analytics** | Multi-format File I/O (CSV, JSON, XML, TXT, Pickle serialization), **Pandas** empirical benchmarking engine (DataFrames, GroupBy aggregations, pivot analysis). |

---

## 📂 Project Organization

```text
Python Mega Project/
├── app.py                      # Streamlit Web Application entry point (Flagship)
├── run_api.py                  # Flask REST API Server launcher (Port 5001)
├── run_gui.py                  # PyQt6 Native Desktop GUI launcher
├── brain.png                   # High-resolution application favicon asset
├── requirements.txt            # Project dependencies
├── .gitignore                  # Git exclusions for Python, caches, and OS artifacts
├── README.md                   # Project documentation and technical manual
└── algolens/                   # Core application package
    ├── __init__.py
    ├── algorithms/             # Algorithm implementations and tracing engine
    │   ├── base.py             # Algorithm, SortingAlgorithm, SearchingAlgorithm ABCs
    │   ├── steps.py            # AlgorithmStep & ExecutionTrace data models
    │   ├── sorting.py          # Quick, Merge, Heap, Insertion, Selection, Bubble Sort
    │   ├── searching.py        # Binary Search, Linear Search
    │   └── registry.py         # AlgorithmRegistry factory pattern
    ├── validation/             # Regex input verification engine
    │   └── validators.py       # InputValidator using Python's `re` module
    ├── data/                   # File handling & serialization
    │   ├── handlers.py         # CSV, JSON, XML, TXT, and Pickle file I/O
    │   └── datasets.py         # Distribution generators (Uniform, Nearly Sorted, Reversed, etc.)
    ├── analytics/              # Empirical performance benchmarking
    │   └── pandas_analysis.py  # Pandas comparative DataFrames and metrics
    ├── visualization/          # Component rendering utilities
    │   ├── array_visualizer.py # Dynamic Bar & SVG Swap Arc renderer
    │   ├── code_highlighter.py # Syntax-highlighted source view generator
    │   ├── state_renderer.py   # State and memory inspector widgets
    │   └── recursion_visualizer.py # Call stack visualizer
    ├── api/                    # Flask REST API implementation
    │   ├── app.py              # Flask app factory with CORS configuration
    │   ├── routes.py           # Endpoints: /health, /algorithms, /execute, /compare, /validate
    │   └── schemas.py          # Trace and step JSON serializers
    ├── gui/                    # PyQt6 Native Desktop GUI implementation
    │   ├── main_window.py      # QMainWindow with timeline controls and code tracker
    │   └── widgets.py          # Custom QPainter ArrayCanvas widget
    ├── static/                 # Single-page web application frontend
    │   └── index.html          # Modern dark-mode IDE interface with Web Audio & SVG graphics
    └── tests/                  # Automated verification suite
        └── test_all.py         # 16 unit tests covering all components
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites & Installation

Clone the repository and install the dependencies in a Python 3.10+ virtual environment:

```bash
# Clone the repository
git clone https://github.com/PseudoBhavya/AlgoVision---Algorithm-Visualizer.git
cd AlgoVision---Algorithm-Visualizer

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate       # On Windows: .venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 2. Launch the Streamlit Web Application (Flagship)

```bash
streamlit run app.py
```
Open your browser at **`http://localhost:8501`**. Experience the full interactive IDE with graph visualization, A* grid, DP table, audio cues, and live source code tracking.

### 3. Launch the Flask REST API Backend

```bash
python3 run_api.py
```
Starts the API service at **`http://127.0.0.1:5001`**.

#### API Endpoints Overview:
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Healthcheck and number of registered algorithms |
| `GET` | `/api/algorithms` | List metadata, time/space complexities for all algorithms |
| `POST` | `/api/execute` | Execute an algorithm on input data and receive full JSON execution trace |
| `POST` | `/api/compare` | Run multiple algorithms on identical data and return comparative metrics |
| `GET` | `/api/datasets` | Fetch predefined benchmark distribution samples |
| `POST` | `/api/validate` | Verify user input arrays against regex rules |

### 4. Launch the Native PyQt6 Desktop GUI

```bash
python3 run_gui.py
```
Launches a standalone desktop window utilizing hardware-accelerated `QPainter` vector graphics.

### 5. Run the Automated Unit Test Suite

```bash
python3 -m unittest algolens/tests/test_all.py
```
Executes all 16 test cases covering algorithm sorting correctness, edge cases (empty lists, duplicates, single elements), search algorithms, regex patterns, file format roundtrips, and REST endpoints.

---

## 🧪 Benchmark & Comparison Arena

Sorted includes an empirical analysis engine powered by **Pandas**:
- **Operation Counting**: Accurately tallies comparisons, swaps, assignments, and recursive depth without timing overhead distortion.
- **Statistical Aggregation**: Computes mean, median, min, max, and standard deviation across multiple trial runs.
- **Speedup Ratios**: Automatically computes normalized speedups against baseline $\mathcal{O}(n^2)$ Bubble Sort.
- **Export Options**: Download benchmark results directly as CSV or JSON for external report compilation.

---

## 👥 Authors & Academic Credits

- **Course**: Bachelor of Computer Applications (BCA) — Advanced Python Programming
- **Project**: End-Semester Capstone Project
- **Architecture**: Clean Architecture / Model-View-Controller (MVC) with Event-Driven Trace Generation

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use it for academic and educational purposes.
