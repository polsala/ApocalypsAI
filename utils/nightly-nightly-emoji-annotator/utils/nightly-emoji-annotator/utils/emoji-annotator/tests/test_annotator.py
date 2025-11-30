import unittest
from emoji_annotator.src.annotator import annotate_line

class TestEmojiAnnotator(unittest.TestCase):
    def test_error_keyword(self):
        self.assertEqual(
            annotate_line("There was an error in the system"),
            "There was an error in the system ❌"
        )

    def test_warning_keyword(self):
        self.assertEqual(
            annotate_line("Warning: low disk space"),
            "Warning: low disk space ⚠️"
        )

    def test_no_keyword(self):
        self.assertEqual(
            annotate_line("Just a regular line"),
            "Just a regular line"
        )

    def test_multiple_keywords_first_match(self):
        # 'error' appears before 'warning' in the map, so ❌ should be used
        self.assertEqual(
            annotate_line("Error and warning detected"),
            "Error and warning detected ❌"
        )

    def test_case_insensitivity(self):
        self.assertEqual(
            annotate_line("TODO: add tests"),
            "TODO: add tests 📝"
        )

# Mock rationale:
# No external resources are accessed; all logic is pure functions.
# Therefore tests are deterministic and offline.

if __name__ == "__main__":
    unittest.main()
