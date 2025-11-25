import unittest
from unittest.mock import patch
import sys
import pathlib

# Ensure src directory is on the import path.
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / 'src'))

# Mock rationale: Ensure deterministic output by controlling random.choice.
# This avoids flaky tests and does not require external resources.

from quote_fetcher import get_random_quote, _QUOTES

class TestQuoteFetcher(unittest.TestCase):
    def test_get_random_quote_returns_known_value(self):
        expected = _QUOTES[2]  # "Dream big and dare to fail."
        with patch('random.choice', return_value=expected):
            result = get_random_quote()
            self.assertEqual(result, expected)

    def test_get_random_quote_is_from_list(self):
        result = get_random_quote()
        self.assertIn(result, _QUOTES)

if __name__ == '__main__':
    unittest.main()
