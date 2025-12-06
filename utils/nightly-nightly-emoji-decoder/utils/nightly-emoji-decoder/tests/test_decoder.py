import unittest
from unittest.mock import patch

# Mock rationale: replace the internal emoji map with a deterministic test‑specific mapping
# so the test does not depend on the production dictionary.

from src.decoder import decode, _EMOJI_MAP

class TestEmojiDecoder(unittest.TestCase):
    def test_basic_decoding(self):
        self.assertEqual(decode("🚀🌕"), "rocket moon")
        self.assertEqual(decode("🧩🔧"), "puzzle wrench")

    def test_unknown_emoji(self):
        # The emoji "🦄" is not in the default map, should become "?"
        self.assertEqual(decode("🦄"), "?")

    def test_custom_mapping_via_mock(self):
        custom_map = {"🦄": "unicorn", "🌈": "rainbow"}
        with patch.object(_EMOJI_MAP, "__getitem__", side_effect=lambda k: custom_map.get(k, "?")):
            # The decoder will now use the mocked __getitem__ behavior
            self.assertEqual(decode("🦄🌈"), "unicorn rainbow")
            self.assertEqual(decode("🚀"), "?")  # original emoji not in custom map

if __name__ == "__main__":
    unittest.main()
