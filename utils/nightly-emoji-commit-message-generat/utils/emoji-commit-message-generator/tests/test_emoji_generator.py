import unittest

# Mock rationale: No external dependencies, deterministic behavior.
from emoji_commit_message_generator.emoji_generator import suggest_emoji, format_commit


class TestEmojiGenerator(unittest.TestCase):
    def test_known_keywords(self):
        cases = [
            ("Add new feature", "✨"),
            ("Fix bug in parser", "🐛"),
            ("Remove deprecated API", "🗑️"),
            ("Update docs for module", "📝"),
            ("Write tests for utils", "✅"),
            ("Refactor code base", "🧹"),
            ("Improve performance of loop", "⚡"),
            ("Setup CI pipeline", "🤖"),
            ("Audit security issue", "🔒"),
        ]
        for msg, expected in cases:
            with self.subTest(msg=msg):
                self.assertEqual(suggest_emoji(msg), expected)

    def test_fallback(self):
        self.assertEqual(suggest_emoji("Random commit message"), "🔧")

    def test_format_commit(self):
        self.assertEqual(
            format_commit("Fix typo in README"),
            "🐛 Fix typo in README"
        )


if __name__ == '__main__':
    unittest.main()
