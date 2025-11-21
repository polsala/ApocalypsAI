import unittest
from utils.nightly_emoji_mood_generator.src import mood

class TestMoodEmoji(unittest.TestCase):
    def test_known_moods(self):
        self.assertEqual(mood.get_emoji("happy"), "😊")
        self.assertEqual(mood.get_emoji("SAD"), "😢")  # case‑insensitive
        self.assertEqual(mood.get_emoji("  excited  "), "🤩")  # whitespace trimmed

    def test_unknown_mood_returns_default(self):
        # Mock rationale: we want deterministic behaviour without external calls.
        self.assertEqual(mood.get_emoji("quantum"), mood.DEFAULT_EMOJI)

    def test_cli_output(self):
        # Mock rationale: capture stdout of the CLI entry point.
        import io, sys
        captured = io.StringIO()
        sys_stdout_original = sys.stdout
        sys.stdout = captured
        try:
            mood.main(["love"])
        finally:
            sys.stdout = sys_stdout_original
        self.assertEqual(captured.getvalue().strip(), "❤️")

if __name__ == "__main__":
    unittest.main()
