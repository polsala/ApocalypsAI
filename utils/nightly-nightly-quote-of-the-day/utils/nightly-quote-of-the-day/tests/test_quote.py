import unittest
from unittest import mock
import datetime

# Mock rationale: we replace datetime.date.today to control the "current" date without network or real time.
# This ensures deterministic, offline tests.

from src.quote import get_quote, _QUOTES

class TestQuoteOfTheDay(unittest.TestCase):
    def test_fixed_date_returns_expected_quote(self):
        # Choose a known date and compute expected index manually.
        test_date = datetime.date(2023, 10, 31)
        # Re‑use the internal seed function via get_quote path.
        # Since _seed_from_date is private, we replicate its logic here.
        import hashlib
        iso = test_date.isoformat().encode("utf-8")
        digest = hashlib.sha256(iso).hexdigest()
        seed = int(digest[:8], 16)
        expected_index = seed % len(_QUOTES)
        expected_quote = _QUOTES[expected_index]
        self.assertEqual(get_quote(test_date), expected_quote)

    @mock.patch('src.quote.datetime.date')
    def test_today_uses_mocked_date(self, mock_date_class):
        # Mock rationale: force datetime.date.today() to return a fixed date.
        mock_today = datetime.date(2022, 1, 1)
        mock_date_class.today.return_value = mock_today
        # Ensure that get_quote() without args uses the mocked today.
        result = get_quote()
        # Compute expected quote using the same logic.
        import hashlib
        iso = mock_today.isoformat().encode('utf-8')
        digest = hashlib.sha256(iso).hexdigest()
        seed = int(digest[:8], 16)
        expected = _QUOTES[seed % len(_QUOTES)]
        self.assertEqual(result, expected)

    def test_invalid_date_cli_argument_exits_gracefully(self):
        # Run the module as a script with an invalid date argument.
        import subprocess, sys, os
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'quote.py'))
        proc = subprocess.run([sys.executable, script_path, '--date', 'invalid-date'], capture_output=True, text=True)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('Invalid date format', proc.stdout + proc.stderr)

if __name__ == '__main__':
    unittest.main()
