import unittest
from src.logger import mood_to_emoji, DEFAULT_EMOJI

class TestEmojiMoodLogger(unittest.TestCase):
    def test_happy_keywords(self):
        self.assertEqual(mood_to_emoji("I am very happy today"), "😄")
        self.assertEqual(mood_to_emoji("Feeling joyful"), "😄")
        self.assertEqual(mood_to_emoji("so glad"), "😊")
        self.assertEqual(mood_to_emoji("excited about the release"), "🤩")

    def test_sad_keywords(self):
        self.assertEqual(mood_to_emoji("I feel sad"), "😢")
        self.assertEqual(mood_to_emoji("down today"), "😔")
        self.assertEqual(mood_to_emoji("depressed about bugs"), "😞")

    def test_angry_keywords(self):
        self.assertEqual(mood_to_emoji("I am angry"), "😠")
        self.assertEqual(mood_to_emoji("mad at the CI"), "😡")
        self.assertEqual(mood_to_emoji("frustrated with merge conflicts"), "😤")

    def test_no_match_returns_default(self):
        # Mock rationale: No mood keywords present, should return neutral face.
        self.assertEqual(mood_to_emoji("just a regular log entry"), DEFAULT_EMOJI)

    def test_multiple_keywords_first_match(self):
        # Mock rationale: "happy" appears before "sad"; first match wins.
        self.assertEqual(mood_to_emoji("I am happy but also sad"), "😄")

if __name__ == "__main__":
    unittest.main()
