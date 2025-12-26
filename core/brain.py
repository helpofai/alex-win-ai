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
        self.researcher = DeepResearcher(self); self.empathy = EmpathyEngine()
        self.correction = CorrectionEngine(); self.reflector = ExperienceReflector(self)
        self.sysadmin = SysAdmin(); self.sandbox = CodeSandbox()
        self.ddgs = DDGS()
        
        self.ceo = CEOBrain(self); self.auth_event = threading.Event(); self.auth_granted = False
        
        # Background init
        self.monitor.start(); threading.Thread(target=self.app_discovery.full_scan, daemon=True).start()
        
        loaded_history = self.memory.load_history()
        self.chat_history = loaded_history if loaded_history else [{"role": "system", "content": self._get_system_prompt()}]
        print("[Universal Navigator] Real-time App Intelligence: ONLINE.")

    def _get_system_prompt(self):
        ctx = self.vision_cortex.get_context_string()
        apps = self.app_discovery.get_app_summary()
        return f"""
        You are Alex, a Universal PC Navigator.
        
        SIGHT (Current Screen): {ctx}
        INSTALLED APPS: {apps}
        
        CAPABILITIES:
        1. Open ANY installed app.
        2. Click ANY text or button you see in 'SIGHT'.
        
        PROTOCOL:
        Use EXECUTE: open [app] | wait [sec] | click text [label]
        Example: To use Calculator: EXECUTE: open calculator | wait 1 | click text 7 | click text + | click text 5
        """

    def process_command(self, command, audio_raw=None):
        if not command: return
        command = command.lower().strip()
        
        if self.use_llm:
            self.chat_history[0]["content"] = self._get_system_prompt()
            response = self.query_lm_studio(command)
            
            if response and "EXECUTE:" in response:
                for line in response.split('\n'):
                    if "EXECUTE:" in line:
                        actions = line.split("EXECUTE:")[1].strip().split("|")
                        action_obj = Action(title=f"Universal Nav: {command[:20]}", desc=response, tool="Navigator", risk_score=self.security.get_risk_score(actions), steps=actions)
                        
                        if self.ui_signals:
                            self.auth_event.clear()
                            self.ui_signals.show_preview.emit(action_obj)
                            self.auth_event.wait()
                            if not self.auth_granted: return "Denied."

                        return self._run_action_chain(action_obj)
                
                self.voice.speak(response); return response

        return self._execute_single_command(command)

    def _run_action_chain(self, action_obj):
        for i, step in enumerate(action_obj.steps):
            step = step.strip()
            if self.ui_signals: self.ui_signals.show_live.emit(i+1, len(action_obj.steps), step, int(((i+1)/len(action_obj.steps))*100))
            
            res = self._execute_single_command(step)
            # Self-Correction logic
            if "not found" in str(res):
                print(f"[Brain] Target '{step}' not found. Refreshing vision...")
                time.sleep(1.0)
                res = self._execute_single_command(step) # Retry after fresh scan
            
            time.sleep(0.5)
        if self.ui_signals: self.ui_signals.show_result.emit("Navigation Successful")
        return "Complete."

    def _execute_single_command(self, action):
        if not action: return
        if self.task_callback: self.task_callback(action)
        print(f"[Executor] {action}")
        
        # --- UNIVERSAL DISCOVERY & NAVIGATION ---
        if action.startswith("click text "):
            target = action.replace("click text ","").strip()
            coords = self.vision_cortex.find_text_coordinates(target)
            if coords:
                self.automation.click_coordinates(coords[0], coords[1])
                return "Success"
            return f"Text '{target}' not found."

        if action.startswith("open "):
            target = action.replace("open ","").strip()
            app_info = self.app_discovery.find_app(target)
            if app_info:
                path = app_info["path"]
                try:
                    if app_info["type"] == "uwp": subprocess.Popen(f"explorer.exe {path}", shell=True)
                    else: os.startfile(path)
                    return "Success"
                except: return "Launch Failed"
            if "." in target: return self.system_ctrl.open_url(target)
            return "App not found."

        # --- STANDARD ---
        if action.startswith("wait "): time.sleep(float(action.split()[1])); return "Done"
        if action.startswith("say "): self.voice.speak(action.replace("say ","").strip())
        if action.startswith("volume "): self.system_ctrl.set_volume(int(action.split()[1]))
        
        return "Handled"

    def set_auth_result(self, granted):
        self.auth_granted = granted; self.auth_event.set()

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
