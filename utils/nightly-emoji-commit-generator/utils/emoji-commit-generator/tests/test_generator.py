import unittest
from src.generator import add_emoji


class TestEmojiGenerator(unittest.TestCase):
    def test_add_keyword(self):
        self.assertEqual(add_emoji("Add new feature"), "✨ Add new feature")

    def test_fix_keyword(self):
        self.assertEqual(add_emoji("Fix bug in parser"), "🐛 Fix bug in parser")

    def test_multiple_keywords_first_match(self):
        # Contains both 'add' and 'fix'; 'add' appears first in EMOJI_MAP.
        self.assertEqual(add_emoji("Add and fix something"), "✨ Add and fix something")

    def test_no_keyword(self):
        self.assertEqual(add_emoji("Initial commit"), "Initial commit")

    def test_case_insensitivity(self):
        self.assertEqual(add_emoji("ReFActOr code base"), "🛠️ ReFActOr code base")


if __name__ == "__main__":
    unittest.main()
