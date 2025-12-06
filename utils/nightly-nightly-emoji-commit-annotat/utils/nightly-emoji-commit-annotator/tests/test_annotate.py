import unittest
import sys
import pathlib

# Ensure the src directory is on the import path
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from src.annotate import annotate, _find_keyword

class TestEmojiAnnotator(unittest.TestCase):
    def test_keyword_mapping(self):
        cases = {
            "Fix bug in parser": "🛠️ Fix bug in parser",
            "Add new feature": "✨ Add new feature",
            "Remove deprecated API": "❌ Remove deprecated API",
            "Refactor module": "♻️ Refactor module",
            "Update docs for API": "📚 Update docs for API",
            "Write tests for edge cases": "✅ Write tests for edge cases",
            "Improve performance of loop": "⚡ Improve performance of loop",
            "Patch security vulnerability": "🔒 Patch security vulnerability",
            "Random commit": "🔧 Random commit",
        }
        for msg, expected in cases.items():
            with self.subTest(msg=msg):
                self.assertEqual(annotate(msg), expected)

    def test_find_keyword_fallback(self):
        kw, emoji = _find_keyword("Just a message")
        self.assertEqual(kw, "")
        self.assertEqual(emoji, "🔧")

    # Mock rationale: no external calls, deterministic behavior.
    # # Mock rationale: ensures test isolation without network.

if __name__ == "__main__":
    unittest.main()
