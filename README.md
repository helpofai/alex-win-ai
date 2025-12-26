# 🛰️ Alex AI: The Agentic OS Core v4.1.0
### *Autonomous. Private. Enterprise-Grade.*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.14+](https://img.shields.io/badge/Python-3.14+-blue.svg)](https://www.python.org/)
[![Security: Zero--Trust](https://img.shields.io/badge/Security-Zero--Trust-red.svg)](#security-model)
[![Architecture: SoC--Brain](https://img.shields.io/badge/Architecture-SoC--Brain-cyan.svg)](#the-society-of-brains)

---

## 🏛️ System Architecture: The Society of Brains
Alex operates via a **Decentralized Agentic Mesh**. Instead of a single model, Alex coordinates a "Society" of specialist agents:
*   **CEO-Brain (Orchestrator)**: The master logic engine using a `Plan-Execute-Reflect` loop.
*   **Visual Cortex**: High-speed local OCR and UI grounding for screen-content awareness.
*   **Memory specialist**: Dual-layer memory (Episodic Experience + Semantic Facts).
*   **SysAdmin specialist**: Direct kernel-level interaction for registry and network operations.

---

## 🔥 Enterprise Features

### 🧠 Autonomous Agentic Intelligence
| Feature | Description |
| :--- | :--- |
| **Recursive Planning** | CEO-Brain generates multi-stage `THOUGHT` and `PLAN` blocks before execution. |
| **Self-Correction** | Real-time monitoring of task outcomes; Alex replans automatically if a command fails. |
| **Self-Evolution** | Alex writes, compiles, and installs its own Python "skills" to expand its native capabilities. |
| **Deep Research** | Multi-source web verification; scrapes top 5 results to cross-reference and detect misinformation. |

### 👁️ Universal UI Navigation
*   **Semantic Grounding**: Can identify and click any UI element based on text description rather than coordinates.
*   **Multi-Monitor Support**: Intelligent popup positioning based on real-time cursor tracking.
*   **Contextual Senses**: Real-time awareness of active windows, system load, and user focus state.

### 🎙️ Total Independence & Hybrid Voice
*   **100% Offline STT**: Powered by **Vosk**; your voice data never leaves your local machine.
*   **Neural TTS**: High-fidelity speech via **Edge TTS** with JARVIS-style emotional modulation.
*   **Emotional Tags**: Supports sync-play reactions like `(laughs)`, `(sighs)`, or `(chuckle)`.

### 🛡️ Zero-Trust Security Model
*   **Risk Scoring**: Every action is assigned a score (0-100). High-risk chains trigger mandatory MFA.
*   **Dual Biometrics**: Secure authorization via **Face ID** (OpenCV) and **Voice Fingerprinting** (Spectral Analysis).
*   **Transparency HUD**: Four distinct window tiers (Preview, Live, Result, Critical) ensure full auditability.

---

## 🚀 Installation & Setup

### 💻 System Requirements
*   **OS**: Windows 10/11 (64-bit).
*   **Python**: v3.10 to v3.14 (Recommended).
*   **Hardware**: 8GB RAM minimum. *GPU acceleration (NVIDIA) recommended for OCR speed.*

### 🛠️ Step-by-Step Deployment
1.  **Initialize Environment**:
    ```powershell
    git clone https://github.com/helpofai/alex-win-ai.git
    cd alex-win-ai
    python -m venv venv
    .\venv\Scripts\activate
    ```
2.  **Install Core Dependencies**:
    ```powershell
    pip install -r requirements.txt
    ```
3.  **Configure Local Brain**:
    Download and launch [LM Studio](https://lmstudio.ai/). Load a model (e.g., Llama 3) and start the **Local Server** on port `1234`.
4.  **First Launch**:
    Execute `run.bat`. Alex will automatically download the **Vosk STT** model (~40MB) on the first run.
5.  **Biometric Enrollment**:
    *   Command: *"Hey Alex, enroll my face."*
    *   Command: *"Hey Alex, enroll my voice."*

---

## 🧑‍💻 Developer Documentation

### 🧱 Specialist API
Developers can extend Alex by adding specialists to the `core/` directory and registering them in the `CEO-Brain`.

#### **Action Schema (The Contract)**
Every action passed to the UI must follow the `Action` object:
```python
Action(title="Task Name", desc="Human-readable intent", tool="SpecialistID", risk_score=50, steps=[])
```

### 🧬 Extending the Skill Graph
Alex populates `data/skills_graph.json` through interaction. You can manually seed the graph to define "God-Mode" shortcuts:
1.  Add entry to `corrections` mapping.
2.  Key: `User Natural Language`.
3.  Value: `EXECUTE: specialist_command`.

### 🧪 Debugging & Logs
*   **Cockpit Terminal**: Real-time logs appear in the bottom dashboard panel.
*   **Episodic Log**: Review `data/episodes.json` to analyze Alex's decision-making history.
*   **Simulation Mode**: Toggle `is_simulation = True` in `core/brain.py` to test plans without OS execution.

---

**Developed by helpofai** | *Pioneering Autonomous Local Intelligence.*
