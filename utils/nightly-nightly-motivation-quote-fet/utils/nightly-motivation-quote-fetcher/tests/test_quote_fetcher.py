import unittest
from unittest.mock import patch

# Mock rationale: we patch `random.choice` to return a deterministic value so the test does not depend on randomness.

from src.quote_fetcher import get_random_quote, _QUOTES


class TestQuoteFetcher(unittest.TestCase):
    def test_get_random_quote_returns_expected_when_mocked(self):
        expected = _QUOTES[2]  # Choose a known element from the list
        with patch('random.choice', return_value=expected) as mock_choice:
            result = get_random_quote()
            mock_choice.assert_called_once_with(_QUOTES)
            self.assertEqual(result, expected)

    def test_quotes_list_is_non_empty(self):
        self.assertTrue(len(_QUOTES) > 0, "Quote list should contain at least one entry")

    def test_all_quotes_are_strings(self):
        for quote in _QUOTES:
            self.assertIsInstance(quote, str)


if __name__ == "__main__":
    unittest.main()
