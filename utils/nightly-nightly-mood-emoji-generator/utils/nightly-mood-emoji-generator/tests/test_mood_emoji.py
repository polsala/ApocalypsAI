import unittest
import sys
import os

# Add the src directory to the import path so we can import the module under test.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from mood_emoji import get_mood_emoji

class TestMoodEmoji(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(
            get_mood_emoji("I am happy and excited about the great news!"),
            "😄",
        )

    def test_negative(self):
        self.assertEqual(
            get_mood_emoji("I feel sad and miserable after the terrible event."),
            "😞",
        )

    def test_neutral(self):
        # Mock rationale: neutral sentence contains no sentiment keywords.
        self.assertEqual(
            get_mood_emoji("The sky is blue and the grass is green."),
            "😐",
        )

if __name__ == "__main__":
    unittest.main()
