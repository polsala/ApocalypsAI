import os
import sys
import unittest

# Ensure the src directory is on the import path
CURRENT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "src"))
sys.path.append(SRC_DIR)

from analyzer import analyze_mood  # type: ignore

class TestEmojiMoodAnalyzer(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(analyze_mood("I am feeling happy and wonderful!"), "😄")

    def test_negative(self):
        self.assertEqual(analyze_mood("This is terrible and I am sad."), "😞")

    def test_mixed(self):
        self.assertEqual(analyze_mood("I love the day but also feel upset."), "😕")

    def test_neutral(self):
        self.assertEqual(analyze_mood("Just an ordinary statement."), "🤔")

if __name__ == "__main__":
    unittest.main()
