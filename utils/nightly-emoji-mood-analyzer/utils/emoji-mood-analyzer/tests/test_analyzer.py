import unittest
import sys
import pathlib

# Adjust import path to locate the src package.
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from analyzer import analyze_mood


class TestEmojiMoodAnalyzer(unittest.TestCase):
    def test_happy(self):
        self.assertEqual(analyze_mood("I am so happy today!"), "😊")

    def test_sad(self):
        self.assertEqual(analyze_mood("Feeling sad about the news."), "😢")

    def test_angry(self):
        self.assertEqual(analyze_mood("He was angry and shouted."), "😠")

    def test_love(self):
        self.assertEqual(analyze_mood("I love this!"), "❤️")

    def test_default(self):
        self.assertEqual(analyze_mood("Just a neutral statement."), "🤔")

    def test_case_insensitivity(self):
        self.assertEqual(analyze_mood("I am HAPPY!"), "😊")

    def test_multiple_keywords(self):
        # The first matching keyword in MOOD_MAP order wins ("happy" before "sad").
        self.assertEqual(analyze_mood("I am happy but also sad."), "😊")

    def test_no_keyword_but_similar(self):
        # "gladly" contains "glad" but as a substring; our simple check still matches.
        self.assertEqual(analyze_mood("She smiled gladly."), "😊")

    def test_unknown_keyword(self):
        # Unknown words should fall back to the default emoji.
        self.assertEqual(analyze_mood("The sky is blue."), "🤔")


if __name__ == "__main__":
    unittest.main()
