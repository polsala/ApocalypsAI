import unittest
from utils.nightly-emoji-mood-analyzer.src.mood import analyze_mood

class TestEmojiMoodAnalyzer(unittest.TestCase):
    def test_happy(self):
        self.assertEqual(analyze_mood("I am happy and excited"), "😊")

    def test_sad(self):
        self.assertEqual(analyze_mood("Feeling sad and lonely today"), "😢")

    def test_angry(self):
        self.assertEqual(analyze_mood("This makes me angry!"), "😠")

    def test_love(self):
        self.assertEqual(analyze_mood("I love this project"), "❤️")

    def test_fear(self):
        self.assertEqual(analyze_mood("I'm terrified of bugs"), "😱")

    def test_neutral(self):
        self.assertEqual(analyze_mood("Just an ordinary day"), "🤔")

if __name__ == "__main__":
    unittest.main()
