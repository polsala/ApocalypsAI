import unittest
from src.mood_meter import get_mood_emoji

class TestMoodMeter(unittest.TestCase):
    def test_positive_over_negative(self):
        # Contains both a positive and a negative keyword; positive wins per spec
        self.assertEqual(get_mood_emoji("I finally fixed the bug!"), "😊")

    def test_negative(self):
        self.assertEqual(get_mood_emoji("This is a terrible error"), "😞")

    def test_angry(self):
        self.assertEqual(get_mood_emoji("I'm so angry about the failure"), "😡")

    def test_default(self):
        self.assertEqual(get_mood_emoji("Just a neutral statement."), "🤔")

    def test_case_insensitivity(self):
        self.assertEqual(get_mood_emoji("LOVE the new feature"), "😊")

if __name__ == "__main__":
    unittest.main()
