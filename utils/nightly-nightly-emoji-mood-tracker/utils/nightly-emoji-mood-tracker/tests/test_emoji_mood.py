import unittest
from src.emoji_mood import get_mood_emoji

class TestEmojiMood(unittest.TestCase):
    def test_happy_sentence(self):
        # Mock rationale: deterministic happy keyword present
        text = "I am feeling great and full of joy today!"
        self.assertEqual(get_mood_emoji(text), "😄")

    def test_sad_sentence(self):
        # Mock rationale: deterministic sad keyword present
        text = "It was a terrible, rainy day and I feel sad."
        self.assertEqual(get_mood_emoji(text), "😢")

    def test_neutral_sentence(self):
        # Mock rationale: no happy or sad keywords
        text = "The meeting lasted two hours and covered the agenda."
        self.assertEqual(get_mood_emoji(text), "😐")

    def test_mixed_keywords_happy_precedence(self):
        # Mock rationale: happy should win if both sets appear
        text = "I love the sunshine but the rain makes me sad."
        self.assertEqual(get_mood_emoji(text), "😄")

if __name__ == "__main__":
    unittest.main()
