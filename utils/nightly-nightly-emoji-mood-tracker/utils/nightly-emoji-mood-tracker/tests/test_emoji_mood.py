import unittest
import sys
import os

# Add src directory to import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from emoji_mood import score_to_emoji


class TestScoreToEmoji(unittest.TestCase):
    def test_valid_mappings(self):
        cases = {
            -10: "😭",
            -8: "😭",
            -6: "😞",
            -4: "😞",
            -2: "😐",
            0: "😐",
            1: "🙂",
            3: "🙂",
            5: "😄",
            7: "😄",
            9: "🤩",
            10: "🤩",
        }
        for score, expected in cases.items():
            with self.subTest(score=score):
                self.assertEqual(score_to_emoji(score), expected)

    def test_out_of_range(self):
        for score in (-11, 11):
            with self.subTest(score=score):
                with self.assertRaises(ValueError):
                    score_to_emoji(score)

    def test_non_integer(self):
        for val in (3.5, "5", None):
            with self.subTest(val=val):
                with self.assertRaises(TypeError):
                    score_to_emoji(val)


if __name__ == "__main__":
    unittest.main()
