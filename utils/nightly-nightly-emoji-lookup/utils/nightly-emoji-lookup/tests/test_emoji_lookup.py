import unittest
from pathlib import Path

# Mock rationale: The emoji dictionary is static and defined in the module, so we can import it directly.
# This ensures the tests are deterministic and require no network access.
from src.emoji_lookup import get_emoji, get_name

class TestEmojiLookup(unittest.TestCase):
    def test_get_emoji_known(self):
        self.assertEqual(get_emoji("rocket"), "🚀")
        self.assertEqual(get_emoji("ROCKET"), "🚀")  # case‑insensitive
        self.assertEqual(get_emoji("smile"), "😄")

    def test_get_emoji_unknown(self):
        self.assertIsNone(get_emoji("nonexistent"))

    def test_get_name_known(self):
        self.assertEqual(get_name("🚀"), "rocket")
        self.assertEqual(get_name("😄"), "smile")

    def test_get_name_unknown(self):
        self.assertIsNone(get_name("🦄"))  # not in our tiny map

    def test_cli_lookup_name(self):
        # Simulate CLI call via subprocess – but to stay offline we invoke the module directly.
        from src import emoji_lookup as mod
        # Capture stdout
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            mod.main.__globals__["_parse_args"] = lambda _: type('Args', (), {'query': 'rocket'})
            try:
                mod.main()
            except SystemExit:
                pass
        self.assertEqual(buf.getvalue().strip(), "🚀")

    def test_cli_lookup_char(self):
        from src import emoji_lookup as mod
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            mod.main.__globals__["_parse_args"] = lambda _: type('Args', (), {'query': '🚀'})
            try:
                mod.main()
            except SystemExit:
                pass
        self.assertEqual(buf.getvalue().strip(), "rocket")

if __name__ == "__main__":
    unittest.main()
