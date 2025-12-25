class EmpathyEngine:
    def __init__(self):
        self.user_mood = "Neutral"
        # Simple keyword-based sentiment for speed
        self.frustration_keywords = ["stop", "shut up", "wrong", "hate", "stupid", "dumb", "no", "bad"]
        self.praise_keywords = ["great", "thanks", "good job", "love", "amazing", "awesome"]

    def analyze_sentiment(self, text):
        """Returns: Frustrated, Happy, or Neutral."""
        text = text.lower()
        
        frustrated_count = sum(1 for word in self.frustration_keywords if word in text)
        praise_count = sum(1 for word in self.praise_keywords if word in text)
        
        if frustrated_count > praise_count:
            self.user_mood = "Frustrated"
        elif praise_count > frustrated_count:
            self.user_mood = "Happy"
        else:
            self.user_mood = "Neutral"
            
        return self.user_mood

    def get_behavioral_adjustment(self, mood):
        if mood == "Frustrated":
            return "The user is frustrated. Be extremely apologetic, brief, and helpful. Do not use humor."
        if mood == "Happy":
            return "The user is happy. Be more expressive, use emojis, and engage in friendly banter."
        return "The user is neutral. Be professional and efficient."
