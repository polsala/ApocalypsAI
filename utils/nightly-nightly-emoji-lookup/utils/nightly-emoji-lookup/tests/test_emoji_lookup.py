import unittest
import os
import sys

# Add the src directory to the import path so the module can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from emoji_lookup import name_to_emoji, emoji_to_name, list_all

class TestEmojiLookup(unittest.TestCase):
    def test_name_to_emoji_known(self):
        self.assertEqual(name_to_emoji(":smile:"), "😄")
        self.assertEqual(name_to_emoji(":fire:"), "🔥")

    def test_name_to_emoji_unknown(self):
        self.assertIsNone(name_to_emoji(":unknown:"))

    def test_emoji_to_name_known(self):
        self.assertEqual(emoji_to_name("👍"), ":thumbs_up:")
        self.assertEqual(emoji_to_name("❤️"), ":heart:")

    def test_emoji_to_name_unknown(self):
        self.assertIsNone(emoji_to_name("🦄"))

    def test_list_all_contains_known(self):
        mapping = list_all()
        self.assertIn(":star:", mapping)
        self.assertEqual(mapping[":star:"], "⭐")
        # Ensure reverse consistency for every entry
        for name, emoji in mapping.items():
            self.assertEqual(emoji_to_name(emoji), name)

if __name__ == "__main__":
    unittest.main()
