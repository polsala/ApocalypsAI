import unittest
from datetime import date

# Mock rationale: Import from the sibling src directory without altering sys.path globally.
# The test runner adds the repository root to PYTHONPATH, so we can use a relative import.
from src.formatter import format_date

class TestEmojiDateFormatter(unittest.TestCase):
    def test_format_known_date(self):
        # December 25 → 🎄📅
        self.assertEqual(format_date(date(2023, 12, 25)), "🎄25📅")

    def test_format_string_input(self):
        # March 1 → 🌱📅
        self.assertEqual(format_date("2024-03-01"), "🌱1📅")

    def test_invalid_string_raises(self):
        with self.assertRaises(ValueError):
            format_date("not-a-date")

    def test_cli_output(self):
        # Mock rationale: Use subprocess to invoke the module as a script.
        import subprocess, sys, os
        cmd = [sys.executable, "-m", "src.formatter", "2022-07-04"]
        result = subprocess.run(
            cmd,
            cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")),
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.stdout.strip(), "🏖️4📅")
        self.assertEqual(result.returncode, 0)

if __name__ == "__main__":
    unittest.main()
