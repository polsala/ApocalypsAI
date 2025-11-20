import unittest
from nightly_emoji_mood_meter import mood_emoji

class TestMoodEmoji(unittest.TestCase):
    def test_positive(self):
        text = "I am happy and love this wonderful sunny day"
        self.assertEqual(mood_emoji(text), "😄")

    def test_negative(self):
        text = "It was a terrible, rainy, and sad evening"
        self.assertEqual(mood_emoji(text), "😞")

    def test_neutral(self):
        text = "The cat sits on the mat"
        self.assertEqual(mood_emoji(text), "🤔")

    def test_equal_counts(self):
        # Mock rationale: equal positive and negative words should yield neutral
        text = "I love but also hate this"
        self.assertEqual(mood_emoji(text), "🤔")

if __name__ == "__main__":
    unittest.main()
