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
        self.sandbox = CodeSandbox(); self.researcher = DeepResearcher(self)
        self.empathy = EmpathyEngine(); self.correction = CorrectionEngine()
        self.reflector = ExperienceReflector(self); self.sysadmin = SysAdmin()
        self.ui_inspector = UIInspector(); self.ddgs = DDGS(); self.ceo = CEOBrain(self)
        
        self.auth_event = threading.Event(); self.auth_granted = False
        self.user_mood = "Neutral"; self.last_command = None; self.pending_correction = False; self.is_enrolling = False
        
        # Start Monitor
        self.monitor.start(); threading.Thread(target=self.app_discovery.full_scan, daemon=True).start()
        
        loaded_history = self.memory.load_history()
        self.chat_history = loaded_history if loaded_history else [{"role": "system", "content": self._get_system_prompt()}]
        print("[Intent Engine] Full System Integration Online.")

    def check_llm_readiness(self):
        try:
            res = requests.get(self.models_url, timeout=2)
            if res.status_code == 200: return "READY", "Connected"
        except: pass
        is_installed = os.path.exists(os.path.join(os.environ["LOCALAPPDATA"], "LM-Studio"))
        if is_installed: return "NOT_CONFIGURED", "Server not running on port 1234."
        return "NOT_INSTALLED", "LM Studio not detected."

    def _get_system_prompt(self):
        ctx = self.vision_cortex.get_context_string()
        apps = self.app_discovery.get_app_summary()
        return f"""
        You are Alex, the CEO-Brain of a high-performance PC AI workstation.
        CONTEXT: {ctx}
        INSTALLED APPS: {apps}
        PROTOCOL: Use EXECUTE: step1 | step2 for actions.
        """

    def process_command(self, command, audio_raw=None):
        if not command: return
        command = command.lower().strip()
        
        # Check readiness
        status, _ = self.check_llm_readiness()
        if status != "READY":
            # Fast-track open commands even without LLM if possible
            if self._is_local_command(command): 
                return self._execute_single_command(command)
            return "Local Brain Offline. Please connect LM Studio."

        # Logging to dashboard
        self._log_to_dashboard("activity", f"Processing: {command}")

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

    def _is_local_command(self, command):
        """Checks if a command can be executed locally without LLM."""
        local_prefixes = ["open ", "volume ", "lock pc", "click text ", "say "]
        return any(command.startswith(p) for p in local_prefixes) or command == "lock pc"

    def _run_action_chain_internal(self, actions, cmd, full_resp, audio_raw):
        score = self.security.get_risk_score(actions)
        action_obj = Action(title=f"Task: {cmd[:20]}", desc=full_resp, tool="Agent Core", risk_score=score, steps=actions)
        if self.ui_signals:
            self.auth_event.clear(); self.ui_signals.show_preview.emit(action_obj); self.auth_event.wait()
            if not self.auth_granted: return
        self._run_action_chain(action_obj)

    def _run_action_chain(self, action_obj):
        total = len(action_obj.steps)
        for i, step in enumerate(action_obj.steps):
            step = step.strip()
            self._log_to_dashboard("activity", f"Executing: {step}")
            if self.ui_signals: self.ui_signals.show_live.emit(i+1, total, step, int(((i+1)/total)*100))
            res = self._execute_single_command(step)
            if self.ui_signals and res: self._log_to_dashboard("data", str(res))
            time.sleep(0.5)
        if self.ui_signals: self.ui_signals.show_result.emit("Task Complete")
        return "Success"

    def _execute_single_command(self, action):
        if not action: return
        if self.task_callback: self.task_callback(action)
        print(f"[Executor] {action}")

        # --- ROUTING ---
        cat = "browser" if any(x in action for x in ["read", "search", "google", "youtube"]) else "files" if "open" in action else "activity"

        if action.startswith("open "):
            target = action.replace("open ","").strip()
            app = self.app_discovery.find_app(target)
            if app:
                path = app["path"]
                self.voice.speak(f"Opening {app['name']}")
                try:
                    cmd = f'powershell -Command "Invoke-Item \'{path}\'"'
                    subprocess.Popen(cmd, shell=True)
                    res = f"Launched {app['name']}"; self._log_to_dashboard("files", res); return res
                except: return "Launch Failed"
            if "." in target: return self.system_ctrl.open_url(target)
            return "App not found."

        if action.startswith("click text "):
            t = action.replace("click text ","").strip()
            c = self.vision_cortex.find_text_coordinates(t)
            if c:
                if self.ui_signals: self.ui_signals.show_ripple.emit(c[0], c[1])
                return self.automation.click_coordinates(c[0], c[1])
            return "Text not found"

        if action.startswith("say "): self.voice.speak(action[4:].strip()); return "Spoken"
        if action.startswith("search "): 
            res = self.researcher.perform_deep_research(action[7:].strip())
            self._log_to_dashboard("browser", res); return res

        if action.startswith("volume "): return self.system_ctrl.set_volume(int(action.split()[1]))
        if action == "lock pc": return self.system_ctrl.lock_pc()
        
        self._log_to_dashboard(cat, f"Action completed: {action}")
        return "Success"

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
            r = requests.post(self.local_server_url, json={"model": self.current_model, "messages": self.chat_history + [{"role":"user","content":p}], "temperature": 0.2}, timeout=20)
            if r.status_code == 200:
                t = r.json()["choices"][0]["message"]["content"].strip()
                self.chat_history.append({"role": "user", "content": p})
                self.chat_history.append({"role": "assistant", "content": t})
                return t
            return None
        except: return None