import unittest
from src.emoji_lookup import get_emoji, main

class TestEmojiLookup(unittest.TestCase):
    def test_exact_match(self):
        self.assertEqual(get_emoji("fire"), "🔥")
        self.assertEqual(get_emoji("Fire"), "🔥")
        self.assertEqual(get_emoji("  fire  "), "🔥")

    def test_multi_word_match(self):
        self.assertEqual(get_emoji("thumbs up"), "👍")
        self.assertEqual(get_emoji("Thumbs Up"), "👍")

    def test_unknown_returns_question(self):
        self.assertEqual(get_emoji("unicorn"), "❓")

    def test_cli_success(self):
        import sys
        original_argv = sys.argv
        try:
            sys.argv = ["emoji_lookup.py", "rocket"]
            from io import StringIO
            import contextlib
            buf = StringIO()
            with contextlib.redirect_stdout(buf):
                exit_code = main()
            self.assertEqual(exit_code, 0)
            self.assertEqual(buf.getvalue().strip(), "🚀")
        finally:
            sys.argv = original_argv

    def test_cli_no_args(self):
        import sys
        original_argv = sys.argv
        try:
            sys.argv = ["emoji_lookup.py"]
            from io import StringIO
            import contextlib
            buf = StringIO()
            with contextlib.redirect_stdout(buf):
                exit_code = main()
            self.assertEqual(exit_code, 2)
            self.assertIn("Usage:", buf.getvalue())
        finally:
            sys.argv = original_argv

if __name__ == "__main__":
    unittest.main()
