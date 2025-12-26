# 🛰️ Alex AI: The Agentic OS Core v4.0
### *Autonomous. Private. Enterprise-Grade.*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.14+](https://img.shields.io/badge/Python-3.14+-blue.svg)](https://www.python.org/)
[![Security: Zero--Trust](https://img.shields.io/badge/Security-Zero--Trust-red.svg)](#security-model)
[![Architecture: SoC--Brain](https://img.shields.io/badge/Architecture-SoC--Brain-cyan.svg)](#the-society-of-brains)

Alex AI is a sophisticated, JARVIS-style autonomous desktop agent designed for secure, high-performance PC orchestration. Utilizing a **Society of Brains (SoC)** architecture, Alex plans, executes, and reflects on complex tasks while maintaining a 100% private local footprint.

---

## 🏛️ System Architecture: The Society of Brains
Alex operates through a coordinated layer of specialist agents managed by a central orchestrator:

1.  **CEO Brain (Orchestrator)**: The primary reasoning engine with a `Plan-Execute-Reflect` loop.
2.  **Visual Cortex**: Local OCR (`EasyOCR`) and UI grounding.
3.  **Security Gate (Zero-Trust)**: Risk-scored actions (0-100) with biometric MFA.
4.  **Specialist Executors**: Multi-tab dashboard for Browser, Files, Debugger, and Network tasks.
5.  **Memory Layer**: Episodic and Semantic memory for persistent learning.

---

## 🔥 Key Capabilities

### 🧠 Autonomous Execution & Self-Evolution
*   **Intent Engine**: Automated multi-step planning and self-correction loop.
*   **Skill Creation**: Alex autonomously writes, installs, and executes Python "skills" (`skills/`) to solve new problems.
*   **PowerShell Protocol**: High-reliability app launching for both classic EXE and UWP Store apps.

### 👁️ Contextual Awareness & Master Dashboard
*   **Command Sphere UI**: A borderless holographic "Cockpit" with real-time system vitals and a floating mini-mode.
*   **Multi-Tab Data Center**: Automatic specialized tabs (Files, Browser, Debugger, Learning) that open and auto-close based on AI activity.
*   **Global Hotkey**: Trigger Alex instantly from anywhere using `Ctrl + Shift + A`.

### 🎙️ Total Offline Independence
*   **Local STT (Vosk)**: 100% offline speech recognition—no data leaves your PC.
*   **Neural TTS (Edge)**: High-quality neural voice with local `pyttsx3` fallback.
*   **Emotional Reactions**: Syncs speech with physical sound effects like `(laughs)` or `(sighs)`.

---

## 🛡️ Security Model
*   **Dual-Biometric Verification**: Face ID (OpenCV) + Voice Fingerprinting (Spectral Analysis).
*   **Transparency HUD**: Real-time "Glass UI" popups for Action Preview, Live Progress, and Critical Alerts.
*   **Critical Confirmation**: High-impact commands require a typed `CONFIRM` code.

---

## 🚀 Installation & Setup

### Prerequisites
- Windows 10/11
- Python 3.10+ (Fully tested on v3.14)
- [LM Studio](https://lmstudio.ai/) (Local server on port 1234)

### Quick Start
1.  **Clone & Install**:
    ```bash
    git clone https://github.com/helpofai/alex-win-ai.git
    cd alex-win-ai
    pip install -r requirements.txt
    ```
2.  **Run**:
    Double-click `run.bat`.
3.  **Enroll**:
    Say: *"Alex, enroll my face"* and *"Alex, enroll my voice."*

---

## 📜 Disclaimer
Alex AI has deep OS access. Use in a trusted environment.

**Developed by helpofai** | *Autonomous Human-PC Interaction.*