import unittest
import sys
import pathlib

# Add the src directory to sys.path so we can import the module
sys.path.append(str(pathlib.Path(__file__).resolve().parents[2] / "src"))

from enhance import enhance_message  # type: ignore

class TestEmojiEnhancer(unittest.TestCase):
    def test_known_keywords(self):
        cases = {
            "fix bug in parser": "🐛 fix bug in parser",
            "Add new feature": "✨ Add new feature",
            "remove deprecated code": "🗑️ remove deprecated code",
            "Update docs for API": "📚 Update docs for API",
            "refactor module": "🔧 refactor module",
            "write tests for edge cases": "✅ write tests for edge cases",
            "chore: bump version": "🔨 chore: bump version",
        }
        for msg, expected in cases.items():
            with self.subTest(msg=msg):
                self.assertEqual(enhance_message(msg), expected)

    def test_no_keyword(self):
        msg = "Improve performance of loop"
        # No matching keyword; should stay unchanged
        self.assertEqual(enhance_message(msg), msg)  # Mock rationale: no keyword mapping

    def test_case_insensitivity(self):
        self.assertEqual(
            enhance_message("FiX something"),
            "🐛 FiX something"
        )

if __name__ == "__main__":
    unittest.main()
