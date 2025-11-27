import io
import sys
import unittest
from unittest.mock import patch

# Mock rationale: we replace `random.choice` to return a deterministic quote,
# ensuring the test is offline, deterministic, and does not depend on the
# actual randomness implementation.

from src.quote_fetcher import get_random_quote, main

class TestQuoteFetcher(unittest.TestCase):
    def test_get_random_quote_mocked(self):
        mock_quote = "Test quote for unit testing."
        with patch('random.choice', return_value=mock_quote):
            self.assertEqual(get_random_quote(), mock_quote)

    def test_main_prints_quote(self):
        mock_quote = "Another deterministic test quote."
        with patch('random.choice', return_value=mock_quote):
            captured_output = io.StringIO()
            sys_stdout = sys.stdout
            try:
                sys.stdout = captured_output
                main()
            finally:
                sys.stdout = sys_stdout
            self.assertEqual(captured_output.getvalue().strip(), mock_quote)

if __name__ == '__main__':
    unittest.main()
