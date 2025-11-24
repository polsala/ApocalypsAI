import unittest
from utils.nightly_emoji_mood_tracker.src import emoji_mood

class TestEmojiMoodDetector(unittest.TestCase):
    def test_happy_detection(self):
        self.assertEqual(emoji_mood.detect_mood("I am feeling wonderful today!"), "😄")

    def test_sad_detection(self):
        self.assertEqual(emoji_mood.detect_mood("It was a gloomy and depressing day."), "😞")

    def test_angry_detection(self):
        self.assertEqual(emoji_mood.detect_mood("I am so mad about the results!"), "😠")

    def test_love_detection(self):
        self.assertEqual(emoji_mood.detect_mood("I love this new feature."), "❤️")

    def test_surprised_detection(self):
        self.assertEqual(emoji_mood.detect_mood("Wow, that was unexpected!"), "😲")

    def test_fear_detection(self):
        self.assertEqual(emoji_mood.detect_mood("I am scared of the upcoming deadline."), "😨")

    def test_neutral_when_no_match(self):
        self.assertEqual(emoji_mood.detect_mood("Just an ordinary sentence without emotion."), "😐")

    # Mock rationale: No external services are called; all logic is pure and deterministic.

if __name__ == "__main__":
    unittest.main()
