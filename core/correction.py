import json
import os

SKILLS_GRAPH = "data/skills_graph.json"

class CorrectionEngine:
    def __init__(self):
        self.graph = self._load_graph()

    def _load_data(self):
        if not os.path.exists(SKILLS_GRAPH):
            default = {"corrections": {}, "success_patterns": {}}
            with open(SKILLS_GRAPH, 'w') as f: json.dump(default, f)
            return default
        try:
            with open(SKILLS_GRAPH, 'r') as f: return json.load(f)
        except: return {"corrections": {}, "success_patterns": {}}

    def _load_graph(self):
        return self._load_data()

    def learn_from_correction(self, failed_intent, corrected_action):
        """Remembers that 'failed_intent' should actually be 'corrected_action'."""
        self.graph["corrections"][failed_intent.lower()] = corrected_action.lower()
        self._save()

    def get_optimized_action(self, intent):
        return self.graph["corrections"].get(intent.lower())

    def _save(self):
        with open(SKILLS_GRAPH, 'w') as f:
            json.dump(self.graph, f, indent=2)

    def summarize_learnings(self):
        count = len(self.graph["corrections"])
        if count == 0: return "System has not needed corrections yet."
        return f"System has learned {count} new intent-to-action mappings."
