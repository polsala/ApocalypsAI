import unittest
from src.emoji_mood import analyze_mood

class TestEmojiMood(unittest.TestCase):
    def test_happy_dominant(self):
        text = "Great job! 😄😄😊"
        self.assertEqual(analyze_mood(text), "happy")

    def test_sad_dominant(self):
        text = "I'm sad 😢😭"
        self.assertEqual(analyze_mood(text), "sad")

    def test_love_dominant(self):
        text = "Love you! ❤️❤️😍"
        self.assertEqual(analyze_mood(text), "love")

    def test_angry_dominant(self):
        text = "This is bad 😡😠"
        self.assertEqual(analyze_mood(text), "angry")

    def test_tie_breaker_priority(self):
        # equal happy and love, love wins per priority
        text = "😊❤️"
        self.assertEqual(analyze_mood(text), "love")

    def test_neutral_when_no_emojis(self):
        text = "Just plain text."
        self.assertEqual(analyze_mood(text), "neutral")

    def test_mixed_counts(self):
        text = "😀😢😢❤️❤️❤️"
        # love count 3, sad count 2, happy 1 => love
        self.assertEqual(analyze_mood(text), "love")

if __name__ == "__main__":
    unittest.main()
