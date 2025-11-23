import unittest
from src.emoji_mood import get_mood_emoji

class TestEmojiMood(unittest.TestCase):
    def test_happy_detection(self):
        # Mock rationale: simple keyword match, deterministic
        self.assertEqual(get_mood_emoji("I am feeling very happy today!"), "😊")
        self.assertEqual(get_mood_emoji("What a fantastic achievement!"), "😊")

    def test_sad_detection(self):
        # Mock rationale: simple keyword match, deterministic
        self.assertEqual(get_mood_emoji("It was a sad day."), "😢")
        self.assertEqual(get_mood_emoji("Feeling down and blue."), "😢")

    def test_angry_detection(self):
        # Mock rationale: simple keyword match, deterministic
        self.assertEqual(get_mood_emoji("I am so angry about this!"), "😠")
        self.assertEqual(get_mood_emoji("That makes me mad."), "😠")

    def test_neutral_when_no_keywords(self):
        # Mock rationale: no matching keywords → neutral emoji
        self.assertEqual(get_mood_emoji("Just an ordinary sentence."), "😐")
        self.assertEqual(get_mood_emoji("The quick brown fox jumps over the lazy dog."), "😐")

if __name__ == "__main__":
    unittest.main()
