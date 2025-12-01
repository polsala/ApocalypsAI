import unittest
from pathlib import Path

# Mock rationale: Import the module directly from the utils folder without installing.
# This keeps the test deterministic and offline.
import sys
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from emoji_committer import enhance_message

class TestEmojiCommitEnhancer(unittest.TestCase):
    def test_fix_keyword(self):
        msg = "Fix typo in README"
        self.assertEqual(enhance_message(msg), "🐛 Fix typo in README")

    def test_feature_keyword(self):
        msg = "Add new feature for user login"
        self.assertEqual(enhance_message(msg), "✨ Add new feature for user login")

    def test_docs_keyword(self):
        msg = "Update docs for API endpoint"
        self.assertEqual(enhance_message(msg), "📝 Update docs for API endpoint")

    def test_no_keyword(self):
        msg = "Random commit without known keywords"
        self.assertEqual(enhance_message(msg), msg)

    def test_multiple_keywords_first_match(self):
        # Both 'test' and 'fix' appear; 'fix' is earlier in the mapping list.
        msg = "Fix failing test for parser"
        self.assertEqual(enhance_message(msg), "🐛 Fix failing test for parser")

    def test_case_insensitivity(self):
        msg = "PERFORMANCE improvements for query engine"
        self.assertEqual(enhance_message(msg), "⚡ PERFORMANCE improvements for query engine")

if __name__ == "__main__":
    unittest.main()
