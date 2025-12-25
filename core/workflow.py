import json
import os
import time

DATA_DIR = "data"
WORKFLOW_FILE = os.path.join(DATA_DIR, "workflows.json")

class WorkflowManager:
    def __init__(self, brain):
        self.brain = brain
        self.workflows = self._load_workflows()

    def _load_workflows(self):
        if not os.path.exists(WORKFLOW_FILE):
            # Default example workflow
            default_data = {
                "coding mode": [
                    {"action": "say", "data": "Initializing coding environment."},
                    {"action": "open", "data": "code"},
                    {"action": "open", "data": "spotify"},
                    {"action": "say", "data": "Ready to code."}
                ],
                "good morning": [
                    {"action": "say", "data": "Good morning, sir."},
                    {"action": "command", "data": "time"},
                    {"action": "command", "data": "date"},
                    {"action": "command", "data": "how is my system doing"}
                ]
            }
            with open(WORKFLOW_FILE, 'w') as f:
                json.dump(default_data, f, indent=2)
            return default_data
        
        try:
            with open(WORKFLOW_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}

    def execute_workflow(self, workflow_name):
        workflow_name = workflow_name.lower()
        if workflow_name not in self.workflows:
            return None
        
        steps = self.workflows[workflow_name]
        self.brain.voice.speak(f"Executing workflow: {workflow_name}")
        
        for step in steps:
            action = step.get("action")
            data = step.get("data")
            
            if action == "say":
                self.brain.voice.speak(data)
                # Wait for speech roughly
                time.sleep(len(data) / 10) 
            
            elif action == "open":
                self.brain.app_manager.open_app(data)
                time.sleep(1)
                
            elif action == "command":
                # Recursive call to brain to handle generic commands
                self.brain.process_command(data)
                time.sleep(1)
                
            elif action == "click":
                self.brain.automation.click_icon(data)
                
            elif action == "type":
                self.brain.automation.type_text(data)

        return f"Workflow {workflow_name} complete."
