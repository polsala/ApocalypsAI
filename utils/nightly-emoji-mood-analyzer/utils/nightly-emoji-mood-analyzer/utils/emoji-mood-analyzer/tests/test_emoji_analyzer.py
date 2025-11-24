import unittest
from src.emoji_analyzer import analyze_mood

class TestEmojiAnalyzer(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(analyze_mood("I love sunny days and great coffee!"), "😊")

    def test_negative(self):
        self.assertEqual(analyze_mood("I hate rainy mornings, they are terrible."), "😞")

    def test_neutral(self):
        self.assertEqual(analyze_mood("The cat sits on the mat."), "😐")

    def test_mixed_more_positive(self):
        self.assertEqual(analyze_mood("I love the weather but the traffic is bad."), "😊")

    def test_mixed_more_negative(self):
        self.assertEqual(analyze_mood("The food is good but the service is terrible and sad."), "😞")

if __name__ == "__main__":
    unittest.main()
