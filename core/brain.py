import requests
import json
import datetime
import os
import subprocess
import webbrowser
import psutil
import platform
import time
import threading
import trafilatura
import re
from duckduckgo_search import DDGS

from core.memory import Memory
from core.automation import Automation
from core.app_discovery import AppDiscovery
from core.workflow import WorkflowManager
from core.system_ops import SystemController
from core.monitor import HealthMonitor
from core.learner import SmartLearner
from core.skills_manager import SkillsManager
from core.vision_cortex import VisionCortex
from core.security import SecurityEngine
from core.biometrics import BiometricEngine
from core.face_id import FaceEngine
from core.episodic_memory import EpisodicMemory
from core.copilot import CodebaseExplorer
from core.sandbox import CodeSandbox
from core.researcher import DeepResearcher
from core.empathy import EmpathyEngine
from core.correction import CorrectionEngine
from core.orchestrator import CEOBrain
from core.reflector import ExperienceReflector
from gui.transparency import Action

class Brain:
    def __init__(self, voice_engine, ui_signals=None, task_callback=None):
        self.voice = voice_engine
        self.ui_signals = ui_signals
        self.task_callback = task_callback
        self.local_server_url = "http://localhost:1234/v1/chat/completions" 
        self.models_url = "http://localhost:1234/v1/models"
        self.use_llm = True
        self.current_model = None
        self.is_active = True 
        
        # Specialist Subsystems
        self.memory = Memory()
        self.automation = Automation()
        self.app_discovery = AppDiscovery()
        self.workflow_manager = WorkflowManager(self)
        self.system_ctrl = SystemController()
        self.learner = SmartLearner()
        self.skills_manager = SkillsManager()
        self.vision_cortex = VisionCortex()
        self.security = SecurityEngine()
        self.biometrics = BiometricEngine()
        self.face_id = FaceEngine()
        self.episodic = EpisodicMemory()
        self.copilot = CodebaseExplorer()
        self.sandbox = CodeSandbox()
        self.researcher = DeepResearcher(self)
        self.empathy = EmpathyEngine()
        self.correction = CorrectionEngine()
        self.reflector = ExperienceReflector(self)
        self.ddgs = DDGS()
        self.ceo = CEOBrain(self)
        
        self.auth_event = threading.Event()
        self.auth_granted = False
        self.user_mood = "Neutral"
        self.last_command = None
        self.pending_correction = False
        self.is_enrolling = False
        
        # Background Initialization
        self.monitor = HealthMonitor(self.alert_system)
        self.monitor.start()
        threading.Thread(target=self.app_discovery.full_scan, daemon=True).start()
        
        loaded_history = self.memory.load_history()
        self.chat_history = loaded_history if loaded_history else [{"role": "system", "content": self._get_system_prompt()}]
        print("[Intent Engine] High-Reliability Mode Online.")

    def _get_system_prompt(self):
        ctx = self.vision_cortex.get_context_string()
        return f"""
        You are Alex, an autonomous PC agent. 
        CONTEXT: {ctx}
        
        CRITICAL: 
        For actions, respond ONLY with "EXECUTE: [cmd]".
        Example: "EXECUTE: open vlc | say opening player"
        Do NOT engage in conversation when an action is requested.
        """

    def process_command(self, command, audio_raw=None):
        if not command: return
        
        # --- 1. CLEANING ---
        raw_cmd = command.lower().strip()
        # Strip filler words
        clean_cmd = re.sub(r'^(hey alex|alex|please|can you|could you)\s+', '', raw_cmd)
        
        print(f"[Brain] Processing: '{clean_cmd}'")

        # --- 2. REGEX FAST-ROUTE (Bypass LLM for 100% Reliability) ---
        # Match "open [app]"
        open_match = re.match(r'^open\s+(.+)', clean_cmd)
        if open_match:
            app_name = open_match.group(1).strip()
            return self._execute_single_command(f"open {app_name}")

        # Match media controls
        if clean_cmd in ["play", "pause", "next", "previous", "stop"]:
            return self._execute_single_command(clean_cmd)

        # Match volume
        vol_match = re.match(r'^(set\s+)?volume\s+(to\s+)?(\d+)', clean_cmd)
        if vol_match:
            return self._execute_single_command(f"volume {vol_match.group(3)}")

        # --- 3. BIOMETRICS ---
        if "enroll my voice" in clean_cmd:
            self.voice.speak("Enrollment active. Speak for 5s."); self.is_enrolling = True; return "Enrolling..."
        if self.is_enrolling and audio_raw is not None:
            res = self.biometrics.enroll(audio_raw); self.is_enrolling = False; self.voice.speak(res); return res

        # --- 4. LLM DEEP BRAIN (For everything else) ---
        if self.use_llm:
            self.chat_history[0]["content"] = self._get_system_prompt()
            response = self.query_lm_studio(clean_cmd)
            
            if response:
                if "EXECUTE:" in response:
                    for line in response.split('\n'):
                        if "EXECUTE:" in line:
                            actions = line.split("EXECUTE:")[1].strip().split("|")
                            action_obj = Action(title=f"Task: {clean_cmd[:20]}", desc=response, tool="Agent Core", risk_score=self.security.get_risk_score(actions), steps=actions)
                            
                            if self.ui_signals:
                                self.auth_event.clear()
                                self.ui_signals.show_preview.emit(action_obj)
                                self.auth_event.wait()
                                if not self.auth_granted: return "Denied."

                            return self._run_action_chain(action_obj)
                
                self.voice.speak(response)
                return response

        return "Command not recognized."

    def _run_action_chain(self, action_obj):
        total = len(action_obj.steps)
        for i, step in enumerate(action_obj.steps):
            step = step.strip()
            if self.ui_signals: self.ui_signals.show_live.emit(i+1, total, step, int(((i+1)/total)*100))
            self._execute_single_command(step)
            time.sleep(0.2)
        if self.ui_signals: self.ui_signals.show_result.emit("Task Complete")
        return "Success"

    def _execute_single_command(self, action):
        if not action: return
        if self.task_callback: self.task_callback(action)
        print(f"[Executor] {action}")
        
        # --- APP LAUNCHER ---
        if action.startswith("open "):
            target = action.replace("open ","").strip()
            app_info = self.app_discovery.find_app(target)
            if app_info:
                path = app_info["path"]
                self.voice.speak(f"Opening {app_info['name']}")
                try:
                    if app_info["type"] == "uwp": subprocess.Popen(f"explorer.exe {path}", shell=True)
                    else: os.startfile(path)
                    return "Success"
                except Exception as e:
                    print(f"Launch error: {e}")
                    return "Launch Failed"
            
            if "." in target: return self.system_ctrl.open_url(target)
            self.voice.speak(f"I couldn't find {target}.")
            return "Not found"

        # --- MEDIA ---
        if action in ["play", "pause", "next", "previous", "stop"]:
            m = {"play":"playpause","pause":"playpause","next":"nexttrack","previous":"prevtrack", "stop":"stop"}
            return self.system_ctrl.media_control(m.get(action, "playpause"))

        # --- OTHERS ---
        if action.startswith("say "): self.voice.speak(action.replace("say ","").strip()); return "Spoken"
        if action.startswith("volume "): self.system_ctrl.set_volume(int(action.split()[1]))
        if action == "lock pc": self.system_ctrl.lock_pc()
        
        return "Done"

    def set_auth_result(self, granted):
        self.auth_granted = granted
        self.auth_event.set()

    def alert_system(self, message):
        self.voice.speak(message)

    def get_active_model(self):
        try:
            r = requests.get(self.models_url, timeout=2)
            if r.status_code == 200:
                m = r.json().get("data", [])
                if m: return m[0].get("id")
        except: pass
        return "local-model" 

    def query_lm_studio(self, prompt):
        try:
            if not self.current_model: self.current_model = self.get_active_model()
            self.chat_history.append({"role": "user", "content": prompt})
            p = {"model": self.current_model, "messages": self.chat_history, "temperature": 0.1, "stream": False}
            res = requests.post(self.local_server_url, json=p, timeout=20)
            if res.status_code == 200:
                t = res.json()['choices'][0]['message']['content'].strip()
                self.chat_history.append({"role": "assistant", "content": t})
                return t
            return None
        except: return None