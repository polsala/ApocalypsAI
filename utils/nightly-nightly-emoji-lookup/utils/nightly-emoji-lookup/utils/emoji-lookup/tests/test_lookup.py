import unittest
from emoji_lookup.lookup import name_to_emoji, emoji_to_name

class TestEmojiLookup(unittest.TestCase):
    def test_name_to_emoji_known(self):
        self.assertEqual(name_to_emoji("smile"), "😄")
        self.assertEqual(name_to_emoji(":thumbsup:"), "👍")

    def test_name_to_emoji_unknown(self):
        self.assertIsNone(name_to_emoji("nonexistent"))

    def test_emoji_to_name_known(self):
        self.assertEqual(emoji_to_name("🔥"), "fire")
        self.assertEqual(emoji_to_name("😀"), "grinning")

    def test_emoji_to_name_unknown(self):
        # 🦄 is not in our tiny map – should return None
        self.assertIsNone(emoji_to_name("🦄"))

if __name__ == "__main__":
    unittest.main()
