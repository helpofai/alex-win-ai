class SecurityEngine:
    def __init__(self):
        # Weights for risk factors
        self.weights = {
            "shutdown": 100,
            "delete": 90,
            "format": 100,
            "create_skill": 85,
            "execute": 80,
            "click": 40,
            "type": 30,
            "open": 20,
            "volume": 5,
            "brightness": 5
        }

    def get_risk_score(self, actions):
        """Calculates a 0-100 score based on the action chain."""
        score = 0
        for action in actions:
            for key, val in self.weights.items():
                if key in action.lower():
                    score = max(score, val)
        return score

    def get_behavior(self, score):
        if score <= 20: return "low"      # Auto-allow
        if score <= 50: return "medium"   # Click allow
        if score <= 80: return "high"     # Confirm popup
        return "critical"                 # Typed confirmation