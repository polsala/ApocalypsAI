import unittest
from unittest.mock import patch

# Mock rationale: we patch random.choice to make the test deterministic and offline.

from src.quote import get_random_quote

class TestDailyMotivationQuote(unittest.TestCase):
    def test_get_random_quote_returns_expected_when_mocked(self):
        expected = "Dream big and dare to fail. – Norman Vaughan"
        with patch('src.quote.random.choice', return_value=expected):
            result = get_random_quote()
            self.assertEqual(result, expected)

    def test_cli_outputs_quote(self):
        expected = "Believe you can and you're halfway there. – Theodore Roosevelt"
        with patch('src.quote.random.choice', return_value=expected), \
             patch('sys.stdout') as mock_stdout:
            # Import the CLI function directly
            from src.quote import _cli
            _cli()
            # Ensure print was called with the expected quote
            mock_stdout.write.assert_any_call(expected + '\n')

if __name__ == '__main__':
    unittest.main()
