import unittest
from emoji_mood_analyzer.src.mood_analyzer import analyze_mood

class TestEmojiMoodAnalyzer(unittest.TestCase):
    def test_happy_keywords(self):
        self.assertEqual(analyze_mood("I am feeling great today!"), "😊")
        self.assertEqual(analyze_mood("What a fantastic event"), "😊")

    def test_sad_keywords(self):
        self.assertEqual(analyze_mood("I am so down right now"), "😢")
        self.assertEqual(analyze_mood("Feeling blue and unhappy"), "😢")

    def test_angry_keywords(self):
        self.assertEqual(analyze_mood("He was furious about the delay"), "😠")
        self.assertEqual(analyze_mood("I'm mad!"), "😠")

    def test_surprised_keywords(self):
        self.assertEqual(analyze_mood("Wow, that was unexpected!"), "😲")
        self.assertEqual(analyze_mood("I am shocked by the news"), "😲")

    def test_default_when_no_match(self):
        self.assertEqual(analyze_mood("Just a neutral statement."), "🤔")

    def test_priority_order(self):
        # "happy" appears before "surprised" in the priority list.
        self.assertEqual(analyze_mood("I am happy and surprised"), "😊")

    def test_case_insensitivity(self):
        self.assertEqual(analyze_mood("I am SAD"), "😢")
        self.assertEqual(analyze_mood("Feeling Joyful"), "😊")

if __name__ == "__main__":
    unittest.main()
