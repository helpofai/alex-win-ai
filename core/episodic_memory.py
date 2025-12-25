import json
import os
import time

EPISODES_FILE = "data/episodes.json"

class EpisodicMemory:
    def __init__(self):
        self.episodes = self._load_data()

    def _load_data(self):
        if not os.path.exists(EPISODES_FILE): return []
        try:
            with open(EPISODES_FILE, 'r') as f: return json.load(f)
        except: return []

    def record_episode(self, command, actions, outcome, rating=5):
        """Records a completed task and its quality."""
        episode = {
            "timestamp": time.time(),
            "command": command,
            "actions": actions,
            "outcome": outcome,
            "rating": rating # 1-5
        }
        self.episodes.append(episode)
        # Keep last 100 episodes
        if len(self.episodes) > 100: self.episodes.pop(0)
        self._save()

    def _save(self):
        with open(EPISODES_FILE, 'w') as f:
            json.dump(self.episodes, f, indent=2)

    def find_similar_experience(self, current_command):
        """Looks for a past successful execution of a similar command."""
        # Simple match for now
        for ep in reversed(self.episodes):
            if ep["command"] == current_command and ep["rating"] >= 4:
                return ep["actions"]
        return None

    def get_performance_summary(self):
        total = len(self.episodes)
        if total == 0: return "No tasks recorded yet."
        avg = sum([e["rating"] for e in self.episodes]) / total
        return f"Processed {total} tasks with an efficiency rating of {avg:.1f}/5.0."
