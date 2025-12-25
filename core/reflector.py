import json
import collections

class ExperienceReflector:
    def __init__(self, brain):
        self.brain = brain

    def analyze_patterns(self):
        """Mines episodic memory for repeated successful sequences."""
        episodes = self.brain.episodic.episodes
        if len(episodes) < 5: return None
        
        # Extract commands
        commands = [e["command"] for e in episodes if e["rating"] >= 4]
        
        # Find frequency
        counts = collections.Counter(commands)
        suggestions = []
        for cmd, count in counts.items():
            if count >= 3: # If you did it 3 times
                suggestions.append(f"Auto-execute '{cmd}' in the future?")
        
        return suggestions

    def generate_optimized_prompt(self):
        """Summarizes top successes to prime the LLM's next session."""
        recent_success = [e["command"] for e in self.brain.episodic.episodes[-10:] if e["rating"] >= 4]
        if not recent_success: return ""
        return f"Recent successful user habits: {', '.join(set(recent_success))}."
