import unittest
from unittest.mock import patch

# Mock rationale: deterministic selection for test – we replace random.choice
# with a lambda that returns a known quote, ensuring the test is offline and repeatable.

from src.zen_quote import get_random_quote, QUOTES


class TestZenQuote(unittest.TestCase):
    def test_get_random_quote_returns_known_value_when_mocked(self):
        expected = QUOTES[0]
        with patch('random.choice', return_value=expected):
            result = get_random_quote()
            self.assertEqual(result, expected)

    def test_quotes_list_is_non_empty(self):
        self.assertTrue(len(QUOTES) > 0, "Quote list should contain at least one entry")


if __name__ == "__main__":
    unittest.main()
