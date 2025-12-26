# 📜 Changelog: Alex AI Agentic Core

## [4.1.0] - 2025-12-23
### 🚀 New Features
- **Universal Semantic Awareness**: Every AI action is now validated against the real-time UI tree and OCR before execution.
- **Deep Window Awareness**: Integrated **Windows UI Automation API** to read internal data from browsers, editors, and Explorer.
- **Physical Control Visuals**: Added a **Neon Ripple Effect** that pulses on screen whenever Alex clicks or drags.
- **Expanded Mouse Primitives**: Added native support for relative movement, right-clicking, and drag-and-drop.
- **Intelligent Error Recovery**: Alex now detects if a click target is missing and reports the specific UI state.

### 🏛️ Architecture & Security
- **Closed-Loop Execution**: Implemented a "Pre-Scan -> Act -> Verify" pipeline for all specialist tasks.
- **PowerShell Reliability**: Further optimized app launching using PowerShell `Invoke-Item` for 100% success rate.

### 🧹 Bug Fixes
- **CFFI Broadcast Fix**: Resolved the final edge cases for audio buffer shape mismatches.
- **Chat Log Sync**: Fixed the background thread routing to ensure all AI thoughts appear in the UI correctly.

---

## [4.0.0] - 2025-12-23
### 🚀 New Features
- **Integrated Command Sphere**: Replaced dashboard with a circular holographic core and "Expanding Wing" panels.
- **Multi-Tab Dashboard**: Implemented a specialized data center with automatic tabs for Files, Browser, and Debugger.
- **Total Offline STT**: Integrated **Vosk** for local speech recognition, removing dependence on Google Cloud.
- **Global Shortcut**: Added `Ctrl + Shift + A` as a system-wide trigger for the cockpit.
- **Mini-Mode**: Created a floating, always-on-top version of the holographic reactor for stealth operation.
- **PowerShell Launch Protocol**: Optimized app launching for Windows shortcuts and Store apps.

### 🏛️ Architecture & Security
- **Orchestrator Refinement**: Improved the `Plan-Execute-Reflect` loop for complex navigation.
- **DPI V2 Support**: Resolved high-DPI scaling issues and "Access Denied" errors on 4K monitors.
- **Spectral Voice ID**: Upgraded voice fingerprinting to 10-point frequency analysis.
- **Critical Authorization**: Added Red Popup gates for high-risk system commands.

### 🧹 Bug Fixes
- **Audio Clipping**: Fixed end-of-sentence clipping via callback-based streaming.
- **CFFI Broadcast Error**: Resolved array shape mismatch in audio playback.
- **App Opening**: Fixed 100% reliability for VLC, Chrome, and system settings.

---
**Identity**: `ALEX AI` | **Build**: `4.0.0-STABLE`
