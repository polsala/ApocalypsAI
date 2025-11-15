import unittest
from datetime import date

# Import the module under test. The relative import works because tests are run with the utils/daily-zen-quote directory on sys.path.
from src.quote import get_daily_quote, main

class TestDailyZenQuote(unittest.TestCase):
    def test_known_dates(self):
        # Known mapping based on the QUOTES list length (10).
        # Day 1 -> index 1 % 10 = 1 -> second quote.
        self.assertEqual(
            get_daily_quote(date(2025, 1, 1)),
            "When the mind is still, the universe surrenders.",
        )
        # Day 10 -> index 10 % 10 = 0 -> first quote.
        self.assertEqual(
            get_daily_quote(date(2025, 1, 10)),
            "The journey of a thousand miles begins with one step.",
        )
        # Leap year day 366 -> index 366 % 10 = 6 -> seventh quote.
        self.assertEqual(
            get_daily_quote(date(2024, 12, 31)),
            "Nature does not hurry, yet everything is accomplished.",
        )

    def test_cli_output(self):
        # Capture stdout from the CLI entry point.
        import io
        import sys

        captured = io.StringIO()
        sys_stdout_original = sys.stdout
        sys.stdout = captured
        try:
            # Simulate CLI with a fixed date.
            main(["--date", "2025-01-01"])
        finally:
            sys.stdout = sys_stdout_original
        output = captured.getvalue().strip()
        self.assertEqual(output, "When the mind is still, the universe surrenders.")

    def test_invalid_date_cli(self):
        # Ensure the CLI exits with code 1 on bad date format.
        import subprocess
        import sys
        # Run the module as a subprocess to capture exit code.
        result = subprocess.run(
            [sys.executable, "-m", "src.quote", "--date", "invalid-date"],
            cwd="../..",  # repository root; tests are executed from utils/daily-zen-quote
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Error: invalid date format", result.stderr)

if __name__ == "__main__":
    unittest.main()
