import unittest
from utils.emoji-commit-message-generator.src.emoji_commit import generate_commit_message

class TestEmojiCommit(unittest.TestCase):
    def test_known_keyword(self):
        # Mock rationale: deterministic mapping ensures stable output.
        self.assertEqual(
            generate_commit_message("fix typo in README"),
            "🛠️ fix typo in README",
        )
        self.assertEqual(
            generate_commit_message("add new feature"),
            "✨ add new feature",
        )
        self.assertEqual(
            generate_commit_message("remove deprecated API"),
            "🗑️ remove deprecated API",
        )

    def test_multiple_keywords_first_match(self):
        # Should pick the first matching keyword in order of appearance.
        self.assertEqual(
            generate_commit_message("refactor and add docs"),
            "🔧 refactor and add docs",
        )

    def test_no_keyword_defaults(self):
        self.assertEqual(
            generate_commit_message("update configuration"),
            "📦 update configuration",
        )

    def test_empty_description_raises(self):
        with self.assertRaises(ValueError):
            generate_commit_message("")

if __name__ == "__main__":
    unittest.main()
