import unittest
from src.emoji_analyzer import analyze_mood

class TestEmojiMoodAnalyzer(unittest.TestCase):
    def test_happy_single(self):
        self.assertEqual(analyze_mood("Great job! 😊"), "happy")

    def test_sad_multiple(self):
        self.assertEqual(analyze_mood("I am sad 😢😞"), "sad")

    def test_angry_mix(self):
        self.assertEqual(analyze_mood("Why? 😡"), "angry")

    def test_neutral_no_emoji(self):
        self.assertEqual(analyze_mood("Just a plain sentence."), "neutral")

    def test_tie_results_neutral(self):
        # Two happy and two sad emojis -> tie
        self.assertEqual(analyze_mood("Mixed feelings 😊😢😊😢"), "neutral")

    def test_dominant_happy_over_others(self):
        # More happy than sad/angry
        self.assertEqual(analyze_mood("Happy 😊😊😢"), "happy")

    # Mock rationale example (no external calls, but showing comment style)
    # Mock rationale: The function does not perform network I/O; all logic is pure.

if __name__ == "__main__":
    unittest.main()
