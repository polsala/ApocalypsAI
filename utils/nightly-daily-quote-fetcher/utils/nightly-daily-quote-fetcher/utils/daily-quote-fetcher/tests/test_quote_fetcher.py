import unittest
from unittest import mock
import sys
import os

# Ensure the src directory is on the import path
CURRENT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "src"))
sys.path.insert(0, SRC_DIR)

from quote_fetcher import get_random_quote, QUOTES

class TestQuoteFetcher(unittest.TestCase):
    @mock.patch('random.choice')
    def test_get_random_quote_returns_mocked(self, mock_choice):
        # Mock rationale: deterministic output for reliable testing
        mock_choice.return_value = QUOTES[0]
        quote = get_random_quote()
        mock_choice.assert_called_once_with(QUOTES)
        self.assertEqual(quote, QUOTES[0])

if __name__ == '__main__':
    unittest.main()
