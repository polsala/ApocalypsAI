import unittest
from src.emoji_commit import generate_message, EMOJI_MAP

class TestEmojiCommit(unittest.TestCase):
    def test_basic_mapping(self):
        # Direct keyword match should yield the mapped emoji.
        self.assertEqual(generate_message(["fix", "login"]), "🐛 fix login")
        self.assertEqual(generate_message(["add", "feature"]), "✨ add feature")
        self.assertEqual(generate_message(["refactor", "module"]), "♻️ refactor module")

    def test_fallback_emoji(self):
        # No matching keyword → default emoji.
        self.assertEqual(generate_message(["unknown", "task"]), "🔧 unknown task")

    def test_case_insensitivity(self):
        # Mapping should be case‑insensitive.
        self.assertEqual(generate_message(["FIX", "issue"]), "🐛 FIX issue")

    def test_empty_keywords_raises(self):
        # Empty list should raise ValueError.
        with self.assertRaises(ValueError):
            generate_message([])

    def test_multiple_matches_uses_first(self):
        # When multiple keywords match, the first in order decides the emoji.
        self.assertEqual(generate_message(["add", "fix"]), "✨ add fix")

    # Mock rationale example (no external calls, but demonstrating mock usage)
    def test_mock_rationale(self):
        # Mock rationale: ensuring deterministic behavior without network.
        # No external dependencies are invoked, so this test remains offline.
        self.assertIn("🐛", EMOJI_MAP.values())

if __name__ == "__main__":
    unittest.main()
