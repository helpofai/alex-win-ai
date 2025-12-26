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
from ddgs import DDGS

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
from core.sysadmin import SysAdmin
from gui.transparency import Action

class Brain:
    def __init__(self, voice_engine, ui_signals=None, task_callback=None):
        self.voice = voice_engine; self.ui_signals = ui_signals; self.task_callback = task_callback
        self.local_server_url = "http://localhost:1234/v1/chat/completions" 
        self.models_url = "http://localhost:1234/v1/models"
        self.use_llm = True; self.current_model = None; self.is_active = True 
        
        # Specialists
        self.memory = Memory(); self.automation = Automation()
        self.app_discovery = AppDiscovery(); self.workflow_manager = WorkflowManager(self)
        self.system_ctrl = SystemController(); self.monitor = HealthMonitor(self.alert_system)
        self.learner = SmartLearner(); self.skills_manager = SkillsManager()
        self.vision_cortex = VisionCortex(); self.security = SecurityEngine()
        self.biometrics = BiometricEngine(); self.face_id = FaceEngine()
        self.episodic = EpisodicMemory(); self.copilot = CodebaseExplorer()
        self.sandbox = CodeSandbox(); self.researcher = DeepResearcher(self)
        self.empathy = EmpathyEngine(); self.correction = CorrectionEngine()
        self.reflector = ExperienceReflector(self); self.sysadmin = SysAdmin()
        self.ddgs = DDGS(); self.ceo = CEOBrain(self)
        
        self.auth_event = threading.Event(); self.auth_granted = False
        self.user_mood = "Neutral"
        self.last_command = None
        self.pending_correction = False
        self.is_enrolling = False
        
        # Start Monitor
        self.monitor.start(); threading.Thread(target=self.app_discovery.full_scan, daemon=True).start()
        
        loaded_history = self.memory.load_history()
        self.chat_history = loaded_history if loaded_history else [{"role": "system", "content": self._get_system_prompt()}]
        print("[Intent Engine] High-Reliability Mode Online.")

    def _get_system_prompt(self):
        ctx = self.vision_cortex.get_context_string()
        apps = self.app_discovery.get_app_summary()
        return f"""
        You are Alex, the CEO-Brain of a high-performance PC AI workstation.
        CONTEXT: {ctx}
        INSTALLED APPS: {apps}
        
        CRITICAL RULES:
        1. If the user wants an action (open, play, click, etc.), you MUST generate an execution plan.
        2. Format actions as "EXECUTE: step1 | step2".
        3. ALWAYS use the full app name from the INSTALLED APPS list in your EXECUTE command.
        """

    def process_command(self, command, audio_raw=None):
        if not command: return
        command = command.lower().strip()
        
        # --- 1. RULE-BASED FAST RESOLVER ---
        if command.startswith("open "):
            target = command.replace("open ", "").strip()
            self._log_to_dashboard("activity", f"Fast-tracking: {target}")
            # Try to execute directly
            res = self._execute_single_command(f"open {target}")
            if "Launched" in res:
                return f"I have opened {target} for you."
            return res

        if self.use_llm:
            self.chat_history[0]["content"] = self._get_system_prompt()
            response = self.query_lm_studio(command)
            
            if response:
                if "EXECUTE:" in response:
                    actions_text = response.split("EXECUTE:")[1].strip().split("|")
                    threading.Thread(target=self._run_action_chain_internal, args=(actions_text, command, response, audio_raw), daemon=True).start()
                    return response
                else:
                    self.voice.speak(response)
                    return response

        return self._execute_single_command(command)

    def _run_action_chain_internal(self, actions, original_cmd, full_response, audio_raw):
        score = self.security.get_risk_score(actions)
        action_obj = Action(title=f"Task: {original_cmd[:20]}", desc=full_response, tool="Agent Core", risk_score=score, steps=actions)
        
        if self.ui_signals:
            self.auth_event.clear()
            self.ui_signals.show_preview.emit(action_obj)
            self.auth_event.wait()
            if not self.auth_granted: return

        self._run_action_chain(action_obj)

    def _run_action_chain(self, action_obj):
        total = len(action_obj.steps)
        for i, step in enumerate(action_obj.steps):
            step = step.strip()
            self._log_to_dashboard("activity", f"Executing: {step}")
            if self.ui_signals: self.ui_signals.show_live.emit(i+1, total, step, int(((i+1)/total)*100))
            self._execute_single_command(step)
            time.sleep(0.5)
        if self.ui_signals: self.ui_signals.show_result.emit("Task Complete")
        return "Success"

    def _execute_single_command(self, action):
        if not action: return
        if self.task_callback: self.task_callback(action)
        print(f"[Executor] {action}")

        # --- SMART APP LAUNCHER ---
        if action.startswith("open "):
            target = action.replace("open ","").strip()
            app_info = self.app_discovery.find_app(target)
            if app_info:
                path = app_info["path"]
                self.voice.speak(f"Opening {app_info['name']}")
                try:
                    if app_info["type"] == "uwp":
                        subprocess.Popen(f'powershell -Command "Start-Process \'{path}\'"', shell=True)
                    else:
                        # Use PowerShell to invoke the shortcut - extremely reliable
                        subprocess.Popen(f'powershell -Command "Invoke-Item \'{path}\'"', shell=True)
                    res = f"Launched {app_info['name']}"
                    self._log_to_dashboard("files", res); return res
                except Exception as e:
                    return f"Launch Error: {e}"
            
            if "." in target: return self.system_ctrl.open_url(target)
            return f"App '{target}' not found."

        # ... (rest of standard handlers)
        if action.startswith("say "): self.voice.speak(action.replace("say ","").strip()); return "Spoken"
        if action in ["play", "pause", "next", "previous", "stop"]:
            m = {"play":"playpause","pause":"playpause","next":"nexttrack","previous":"prevtrack", "stop":"stop"}
            return self.system_ctrl.media_control(m.get(action, "playpause"))
        
        return "Success"

    def _log_to_dashboard(self, category, text):
        if self.ui_signals: self.ui_signals.log_tab.emit(category, text)

    def set_auth_result(self, granted):
        self.auth_granted = granted; self.auth_event.set()

    def alert_system(self, message):
        self.voice.speak(message)

    def get_active_model(self):
        try:
            r = requests.get(self.models_url, timeout=2)
            return r.json().get("data", [])[0].get("id") if r.status_code == 200 else "local-model"
        except: return "local-model" 

    def query_lm_studio(self, prompt):
        try:
            if not self.current_model: self.current_model = self.get_active_model()
            self.chat_history.append({"role": "user", "content": prompt})
            p = {"model": self.current_model, "messages": self.chat_history, "temperature": 0.2, "stream": False}
            res = requests.post(self.local_server_url, json=p, timeout=20)
            if res.status_code == 200:
                t = res.json()['choices'][0]['message']['content'].strip()
                self.chat_history.append({"role": "assistant", "content": t})
                return t
            return None
        except: return None

    def query_lm_studio_vision_coords(self, target, img):
        try:
            p = {"model": self.current_model or "local-model", "messages": [{"role":"user","content":[{"type":"text","text":f"Find {target}. Return [x, y]."},{"type":"image_url","image_url":{"url":img}}]}], "temperature":0.1}
            r = requests.post(self.local_server_url, json=p, timeout=20)
            if r.status_code == 200:
                import ast
                return ast.literal_eval(r.json()['choices'][0]['message']['content'])
        except: return None

    def query_lm_studio_vision(self, prompt, img):
        try:
            p = {"model": self.current_model or "local-model", "messages": [{"role":"user","content":[{"type":"text","text":prompt},{"type":"image_url","image_url":{"url":img}}]}], "temperature":0.7}
            r = requests.post(self.local_server_url, json=p, timeout=25)
            return r.json()['choices'][0]['message']['content'] if r.status_code == 200 else None
        except: return None
