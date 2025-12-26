# 🛰️ Alex AI: The Agentic OS Core v4.0
### *Autonomous. Private. Enterprise-Grade.*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Security: Zero--Trust](https://img.shields.io/badge/Security-Zero--Trust-red.svg)](#security-model)
[![Architecture: SoC--Brain](https://img.shields.io/badge/Architecture-SoC--Brain-cyan.svg)](#the-society-of-brains)

Alex AI is a sophisticated, JARVIS-style autonomous desktop agent designed for secure, high-performance PC orchestration. Unlike standard chatbots, Alex utilizes a **Society of Brains (SoC)** architecture to plan, execute, and reflect on complex multi-step tasks across your entire Windows ecosystem—all while maintaining a strictly local and private data footprint.

---

## 🏛️ System Architecture: The Society of Brains
Alex operates through a coordinated layer of specialist agents managed by a central orchestrator:

1.  **CEO Brain (Orchestrator)**: The primary reasoning engine. It converts human intent into strategic multi-step plans using a `Plan-Execute-Reflect` loop.
2.  **Visual Cortex**: Real-time screen awareness via local OCR (`EasyOCR`) and UI grounding. Alex "sees" what you see to interact with any application.
3.  **Security Gate (Zero-Trust)**: A military-grade filter that risk-scores every action (0-100).
4.  **Specialist Executors**: Dedicated modules for Browser Automation, App Discovery (UWP + EXE), System Operations, and File Management.
5.  **Memory Layer**: Comprising **Episodic Memory** (past experiences) and **Semantic Memory** (learned facts and user habits).

---

## 🔥 Key Capabilities

### 🧠 Autonomous Execution
*   **Intent Decomposition**: Give complex commands like *"Find the latest tech news, save it to a file, and then open my code editor."* Alex plans and chains these actions automatically.
*   **Self-Correction**: If a task fails, Alex analyzes the error logs, re-plans, and retries with a new strategy.
*   **Self-Evolution**: Alex can write, install, and execute its own Python "skills" to expand its capabilities on the fly.

### 👁️ Contextual Awareness
*   **Semantic Clicking**: Alex can find and click buttons based on their text description using local computer vision.
*   **Live OCR**: Real-time extraction of screen text for debugging, research, and summarization.
*   **Focus-Awareness**: Alex monitors your active applications. If you are in an IDE or a game, he enters "Tactical Mode," reducing interruptions and speaking only for critical alerts.

---

## 🛡️ Security Model: Military-Grade
Alex is built on a **Zero-Trust** foundation to ensure the AI remains an asset, never a liability.

*   **Risk Classification**: Actions are categorized into Low, Medium, High, and Critical.
*   **Dual-Biometric Verification**:
    *   **Face ID**: High-security tasks require visual identification via OpenCV.
    *   **Voice Fingerprinting**: Uses spectral analysis to verify the user's unique vocal profile.
*   **Transparency HUD**: Every autonomous move is displayed in a semi-transparent "Glass UI" popup for real-time auditability.
*   **Critical Confirmation**: Actions like file deletion or system shutdown require an explicit, typed `CONFIRM` code from the authorized user.

---

## 🛠️ Advanced Developer Guide

### 🧱 Modular Specialist Architecture
Alex is designed for infinite expansion. The core logic is decoupled into "Specialist Brains." To add a new capability, you don't modify the core; you add a new Specialist.

#### **Adding a New "Skill" (Hot-Loading)**
Alex can autonomously create skills, but you can also manually add them to the `skills/` directory. A skill is a standalone Python script that the **CEO Brain** can call.
1.  Place your script in `skills/my_tool.py`.
2.  The script can use standard library or project utilities.
3.  Execute via voice: *"Alex, run skill my_tool."*

#### **Extending the Intent Engine**
To add a new native command to the **Specialist Execution Layer**:
1.  Open `core/brain.py`.
2.  Add a handler in `_execute_single_command(self, action)`.
3.  Example:
    ```python
    if action.startswith("fire_lasers"):
        return self.hardware_controller.trigger_relay()
    ```

### 🧬 Biometric Enrollment API
Developers must enroll their identity before Alex grants access to `High` or `Critical` risk tiers.
- **Voice Enrollment**: Trigger `self.biometrics.enroll(audio_data)`. Internally, this generates a 10-point spectral envelope.
- **Face Enrollment**: Trigger `self.face_id.enroll()`. This captures 30 samples and trains a local LBPH model.

### 🪟 Transparency HUD Integration
Every specialist action should be reported to the HUD for auditability. Use the `task_callback`:
```python
if self.task_callback:
    self.task_callback("Optimizing Database...")
```

### 🧪 Debugging & Simulation
Toggle **Simulation Mode** in the config to preview all actions in the HUD without real-world execution. Use the **Developer Co-Pilot** to visually debug runtime errors in the Alex console itself.

---

## 🚀 Installation & Setup

### Prerequisites
- Windows 10/11
- Python 3.10 or higher
- [LM Studio](https://lmstudio.ai/) (Running a local model server on port 1234)
- *Recommended: An NVIDIA GPU with 8GB+ VRAM for optimal Vision/OCR performance.*

### Quick Start
1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/helpofai/alex-win-ai.git
    cd alex-win-ai
    ```
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Connect the Brain**:
    Open LM Studio, load a model (e.g., Llama 3 or LLaVA for vision), and start the Local Server.
4.  **Initialize Alex**:
    Double-click `run.bat` or execute `python main.py`.

---

## 📜 Disclaimer & Safety
This system has direct access to your PC's inputs and file system. Always run Alex in a trusted environment. The built-in Zero-Trust model is designed to mitigate risk, but the user remains responsible for the AI's execution path.

**Developed by helpofai** | *Building the future of Autonomous Human-PC Interaction.*
