import json
import os

LEARNED_DATA = "data/learned.json"

class SmartLearner:
    def __init__(self):
        self.data = self._load_data()

    def _load_data(self):
        if not os.path.exists(LEARNED_DATA):
            default = {"mappings": {}, "patterns": [], "failed_commands": []}
            with open(LEARNED_DATA, 'w') as f: json.dump(default, f)
            return default
        try:
            with open(LEARNED_DATA, 'r') as f: return json.load(f)
        except: return {"mappings": {}, "patterns": [], "failed_commands": []}

    def save(self):
        with open(LEARNED_DATA, 'w') as f:
            json.dump(self.data, f, indent=2)

    def learn_mapping(self, natural_phrase, command):
        """Learns that 'phrase' actually means 'command'."""
        self.data["mappings"][natural_phrase.lower()] = command.lower()
        self.save()

    def get_mapped_command(self, phrase):
        return self.data["mappings"].get(phrase.lower())

    def log_failure(self, command):
        self.data["failed_commands"].append(command)
        if len(self.data["failed_commands"]) > 50:
            self.data["failed_commands"].pop(0)
        self.save()

    def suggest_automation(self, recent_history):
        """Analyzes history for repeated sequences."""
        # Simple implementation: look for the same commands in order
        if len(recent_history) < 3: return None
        
        # Logic to find if same 3 apps opened frequently
        # For now, placeholder for real pattern matching
        return None
