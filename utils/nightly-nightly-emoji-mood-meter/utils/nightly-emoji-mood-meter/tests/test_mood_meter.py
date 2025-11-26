import unittest
from src.mood_meter import analyze_mood

class TestMoodMeter(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(analyze_mood("I love this wonderful day!"), "😊")

    def test_negative(self):
        self.assertEqual(analyze_mood("I hate this terrible weather."), "😞")

    def test_neutral(self):
        self.assertEqual(analyze_mood("The cat sits on the mat."), "😐")

    def test_mixed_equal_counts(self):
        # Two positive words, two negative words → tie → neutral
        self.assertEqual(analyze_mood("I love the food but hate the service."), "😐")

    # Mock rationale: No external services are called; the logic is deterministic and fully offline.

if __name__ == "__main__":
    unittest.main()
