import unittest
from unittest.mock import patch

# Mock rationale: we patch `random.choice` to return a deterministic value,
# ensuring the test does not depend on randomness or external state.

from daily_quote_dispenser.src.quote import get_random_quote, QUOTES


class TestQuoteDispenser(unittest.TestCase):
    def test_get_random_quote_returns_expected_when_mocked(self):
        expected = QUOTES[2]  # "The purpose of our lives is to be happy. – Dalai Lama"
        with patch('random.choice', return_value=expected) as mock_choice:
            result = get_random_quote()
            mock_choice.assert_called_once_with(QUOTES)
            self.assertEqual(result, expected)

    def test_quotes_list_is_non_empty(self):
        self.assertTrue(len(QUOTES) > 0, "Quote list should contain at least one entry")


if __name__ == "__main__":
    unittest.main()
