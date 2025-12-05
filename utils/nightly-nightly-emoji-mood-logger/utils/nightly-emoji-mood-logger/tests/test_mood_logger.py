import unittest
from src.mood_logger import analyze_mood

class TestMoodLogger(unittest.TestCase):
    def test_positive(self):
        text = "I am happy and joyful, everything is wonderful and great!"
        self.assertEqual(analyze_mood(text), "😊")

    def test_negative(self):
        text = "I feel sad and depressed, it was a terrible day."
        self.assertEqual(analyze_mood(text), "😢")

    def test_neutral(self):
        text = "I am happy but also a bit sad about the news."
        # equal positive and negative counts => neutral
        self.assertEqual(analyze_mood(text), "😐")

    def test_mixed_more_positive(self):
        text = "Good and great things happened, but the bad was minor."
        self.assertEqual(analyze_mood(text), "😊")

    def test_mixed_more_negative(self):
        text = "Sad and terrible events occurred, but there was a tiny happy moment."
        self.assertEqual(analyze_mood(text), "😢")

if __name__ == "__main__":
    unittest.main()
