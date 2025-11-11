import os
import sys
import unittest

# Ensure the src directory is on the import path.
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from emoji_lookup import shortcode_to_emoji, emoji_to_shortcode

class TestEmojiLookup(unittest.TestCase):
    def test_shortcode_to_emoji_known(self):
        self.assertEqual(shortcode_to_emoji(":smile:"), "😄")
        self.assertEqual(shortcode_to_emoji(":rocket:"), "🚀")

    def test_shortcode_to_emoji_unknown(self):
        self.assertIsNone(shortcode_to_emoji(":unknown:"))

    def test_emoji_to_shortcode_known(self):
        self.assertEqual(emoji_to_shortcode("👍"), ":thumbsup:")
        self.assertEqual(emoji_to_shortcode("☕"), ":coffee:")

    def test_emoji_to_shortcode_unknown(self):
        self.assertIsNone(emoji_to_shortcode("🦄"))

    # Mock rationale: No external services are called; all data lives in‑memory.
    # Therefore tests are deterministic and offline.

if __name__ == "__main__":
    unittest.main()
