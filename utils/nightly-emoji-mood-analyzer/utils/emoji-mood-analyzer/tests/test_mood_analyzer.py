import os
import sys
import unittest

# Add the src directory to the import path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from mood_analyzer import analyze_mood

class TestMoodAnalyzer(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(analyze_mood("I love sunny days and wonderful weather!"), "😊")

    def test_negative(self):
        self.assertEqual(analyze_mood("I hate rainy and gloomy afternoons."), "😞")

    def test_neutral(self):
        self.assertEqual(analyze_mood("The cat sits on the mat."), "😐")

    def test_mixed_more_positive(self):
        self.assertEqual(analyze_mood("I love pizza but hate broccoli."), "😊")

    def test_mixed_more_negative(self):
        self.assertEqual(
            analyze_mood(
                "I love pizza but the service was terrible and the place was dark."
            ),
            "😞",
        )

    # Mock rationale: No external services are called; the logic is deterministic and fully offline.

if __name__ == "__main__":
    unittest.main()
