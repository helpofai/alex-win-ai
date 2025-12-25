# Alex AI - Local Desktop Assistant

A privacy-focused, Jarvis-like AI assistant that runs on your PC.

## Features
- **Local Control**: Works offline for system commands (Time, Date, Apps).
- **Hybrid Brain**: Connects to local LLMs (like Ollama) for intelligence.
- **Voice**: Text-to-Speech (Offline) and Voice Control (Microphone).
- **GUI**: Modern dark-themed interface.

## Quick Start
1.  **Run the Assistant**: Double-click `run.bat` (or run `python main.py`).
2.  **Voice Mode**: Speak commands if your microphone is detected.
3.  **Text Mode**: Type commands in the bottom bar.

## Setting up the "Brain" (Optional)
To make Alex smart (chat about anything), install [Ollama](https://ollama.com/) and run:
```cmd
ollama run llama3
```
Alex will automatically connect to it!

## Common Commands
- "What time is it?"
- "Open Notepad"
- "Open Browser"
- (With Ollama) "Tell me a joke" or "Write a python script..."
