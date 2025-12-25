import json
import os

DATA_DIR = "data"
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")
FACTS_FILE = os.path.join(DATA_DIR, "facts.json")

class Memory:
    def __init__(self):
        self._ensure_files()

    def _ensure_files(self):
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        if not os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'w') as f: json.dump([], f)
        if not os.path.exists(FACTS_FILE):
            with open(FACTS_FILE, 'w') as f: json.dump([], f)

    def load_history(self):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return []

    def save_history(self, history):
        # Keep only last 20 messages to prevent infinite growth
        trimmed = history[-20:] if len(history) > 20 else history
        with open(HISTORY_FILE, 'w') as f:
            json.dump(trimmed, f, indent=2)

    def load_facts(self):
        try:
            with open(FACTS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []

    def add_fact(self, fact_text):
        facts = self.load_facts()
        if fact_text not in facts:
            facts.append(fact_text)
            with open(FACTS_FILE, 'w') as f:
                json.dump(facts, f, indent=2)
            return True
        return False

    def get_facts_as_string(self):
        facts = self.load_facts()
        if not facts:
            return ""
        return "User Facts:\n" + "\n".join([f"- {f}" for f in facts])
