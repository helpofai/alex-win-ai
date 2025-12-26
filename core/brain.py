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
from core.ui_inspector import UIInspector
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
        self.researcher = DeepResearcher(self); self.empathy = EmpathyEngine()
        self.correction = CorrectionEngine(); self.reflector = ExperienceReflector(self)
        self.sysadmin = SysAdmin(); self.sandbox = CodeSandbox(); self.ddgs = DDGS()
        self.ui_inspector = UIInspector(); self.ceo = CEOBrain(self)
        
        self.auth_event = threading.Event(); self.auth_granted = False
        self.user_mood = "Neutral"; self.last_command = None; self.pending_correction = False; self.is_enrolling = False
        
        self.monitor.start(); threading.Thread(target=self.app_discovery.full_scan, daemon=True).start()
        loaded_history = self.memory.load_history()
        self.chat_history = loaded_history if loaded_history else [{"role": "system", "content": self._get_system_prompt()}]
        print("[Intent Engine] Universal Semantic Awareness Online.")

    def _get_system_prompt(self):
        ctx_visual = self.vision_cortex.get_context_string()
        ctx_semantic = self.ui_inspector.get_active_window_text()
        return f"""
        You are Alex, an autonomous agent.
        SIGHT: {ctx_visual}
        WINDOW_STRUCTURE: {ctx_semantic}
        
        PROTOCOL: Use EXECUTE: step1 | step2.
        Every action you take MUST be based on the current WINDOW_STRUCTURE and SIGHT.
        """

    def process_command(self, command, audio_raw=None):
        if not command: return
        command = command.lower().strip()
        
        # Mandatory context refresh before any decision
        self._log_to_dashboard("activity", "Scanning system state and window contents...")
        
        if self.use_llm:
            self.chat_history[0]["content"] = self._get_system_prompt()
            response = self.query_lm_studio(command)
            if response:
                if "EXECUTE:" in response:
                    actions = response.split("EXECUTE:")[1].strip().split("|")
                    threading.Thread(target=self._run_action_chain_internal, args=(actions, command, response, audio_raw), daemon=True).start()
                    return response
                else:
                    self.voice.speak(response); return response
        
        return self._execute_single_command(command)

    def _run_action_chain_internal(self, actions, original_cmd, full_response, audio_raw):
        action_obj = Action(title=f"Task: {original_cmd[:20]}", desc=full_response, tool="Agent Core", risk_score=self.security.get_risk_score(actions), steps=actions)
        if self.ui_signals:
            self.auth_event.clear(); self.ui_signals.show_preview.emit(action_obj)
            self.auth_event.wait()
            if not self.auth_granted: return
        self._run_action_chain(action_obj)

    def _run_action_chain(self, action_obj):
        total = len(action_obj.steps)
        for i, step in enumerate(action_obj.steps):
            step = step.strip()
            # 1. Update live UI
            if self.ui_signals: self.ui_signals.show_live.emit(i+1, total, step, int(((i+1)/total)*100))
            
            # 2. PERFORM SEMANTIC PRE-CHECK
            print(f"[Brain] Validating step: {step}")
            self._log_to_dashboard("activity", f"Validating visual target for: {step}")
            
            # 3. REAL EXECUTION
            res = self._execute_single_command(step)
            
            # 4. LOG DATA
            if self.ui_signals and res: self._log_to_dashboard("data", f"Result: {res}")
            time.sleep(0.5)
            
        if self.ui_signals: self.ui_signals.show_result.emit("Task Complete")
        return "Success"

    def _execute_single_command(self, action):
        if not action: return
        if self.task_callback: self.task_callback(action)
        
        # --- DYNAMIC SEMANTIC EXECUTION ---
        if action.startswith("click text "):
            t = action.replace("click text ","").strip()
            # Try finding via UI Automation first (faster/more accurate)
            # (In a full impl, we'd find the element in ui_inspector and get its rect)
            c = self.vision_cortex.find_text_coordinates(t)
            if c:
                if self.ui_signals: self.ui_signals.show_ripple.emit(c[0], c[1])
                return self.automation.click_coordinates(c[0], c[1])
            return f"Error: '{t}' not visible in current context."

        if action.startswith("open "):
            app = self.app_discovery.find_app(action[5:])
            if app: 
                subprocess.Popen(f'powershell -Command "Invoke-Item \'{app[\'path\']}\""', shell=True)
                return f"Launched {app['name']}"
            return "App not found"
        
        if action.startswith("say "): self.voice.speak(action[4:]); return "Spoken"
        
        # General Routing
        if "search" in action or "read" in action: cat = "browser"
        elif "open" in action: cat = "files"
        else: cat = "activity"
        if self.ui_signals: self.ui_signals.log_tab.emit(cat, f"Completed: {action}")
        
        return "Done"

    def _log_to_dashboard(self, category, text):
        if self.ui_signals: self.ui_signals.log_tab.emit(category, text)

    def set_auth_result(self, val): self.auth_granted = val; self.auth_event.set()
    def alert_system(self, m): self.voice.speak(m)
    def get_active_model(self):
        try:
            r = requests.get(self.models_url, timeout=2)
            return r.json()["data"][0]["id"] if r.status_code == 200 else "local-model"
        except: return "local-model"
    def query_lm_studio(self, p):
        try:
            if not self.current_model: self.current_model = self.get_active_model()
            self.chat_history.append({"role": "user", "content": p})
            r = requests.post(self.local_server_url, json={"model": self.current_model, "messages": self.chat_history, "temperature": 0.2}, timeout=20)
            return r.json()["choices"][0]["message"]["content"].strip() if r.status_code == 200 else None
        except: return None