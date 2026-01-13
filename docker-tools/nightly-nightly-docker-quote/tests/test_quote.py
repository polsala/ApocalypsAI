import unittest
import subprocess
import sys
import pathlib
import os

class TestQuote(unittest.TestCase):
    def test_quote_output(self):
        # Use the script directly
        script = pathlib.Path(__file__).parent.parent / "src" / "quote.py"
        result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        output = result.stdout.strip()
        # The output should be one of the quotes
        expected_quotes = [
            "The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt",
            "Life is what happens when you're busy making other plans. - John Lennon",
            "In the end, we only regret the chances we didn't take. - Unknown",
        ]
        self.assertIn(output, expected_quotes)

    def test_no_quotes(self):
        # Temporarily rename quotes.txt
        script_dir = pathlib.Path(__file__).parent.parent / "src"
        quotes_file = script_dir / "quotes.txt"
        backup = script_dir / "quotes.txt.bak"
        quotes_file.rename(backup)
        try:
            result = subprocess.run([sys.executable, str(script_dir / "quote.py")], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("No quotes found.", result.stderr)
        finally:
            backup.rename(quotes_file)

if __name__ == "__main__":
    unittest.main()
