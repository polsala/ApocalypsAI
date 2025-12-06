import unittest
from utils.nightly_emoji_commit_generator.src.main import get_emoji_for_message

class TestEmojiCommitGenerator(unittest.TestCase):
    def test_known_keywords(self):
        cases = {
            "Fix bug in parser": "🐛",
            "Add new endpoint": "✨",
            "Remove deprecated flag": "🗑️",
            "Refactor authentication flow": "🔧",
            "Update docs for API": "📚",
            "Write tests for utils": "✅",
            "Improve perf of loop": "⚡",
            "CI: add github actions": "🤖",
            "Style: reformat code": "🎨",
            "Chore: bump version": "🧹",
        }
        for msg, expected in cases.items():
            with self.subTest(msg=msg):
                self.assertEqual(get_emoji_for_message(msg), expected)

    def test_fallback(self):
        # Mock rationale: deterministic fallback when no keyword matches.
        self.assertEqual(get_emoji_for_message("Random commit without keyword"), "🎉")

if __name__ == "__main__":
    unittest.main()
