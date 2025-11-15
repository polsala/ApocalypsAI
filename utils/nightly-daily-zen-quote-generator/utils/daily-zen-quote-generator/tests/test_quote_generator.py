import unittest
from unittest.mock import patch

# Mock rationale: deterministic selection for test – we replace random.choice
# with a lambda that returns the first element of the provided list.

from utils.daily_zen_quote_generator.src.quote_generator import get_random_quote, QUOTES


class TestQuoteGenerator(unittest.TestCase):
    def setUp(self):
        # Ensure we have a known ordering for the tests.
        self.quotes = QUOTES

    @patch('random.choice', side_effect=lambda seq: seq[0])
    def test_get_random_quote_no_tag(self, mock_choice):
        # Expect the first quote in the full list.
        expected = self.quotes[0]["text"]
        result = get_random_quote()
        self.assertEqual(result, expected)
        mock_choice.assert_called_once()

    @patch('random.choice', side_effect=lambda seq: seq[0])
    def test_get_random_quote_with_tag(self, mock_choice):
        # Filter by 'humor' – the first matching quote should be returned.
        expected = next(q for q in self.quotes if "humor" in q["tags"])["text"]
        result = get_random_quote(tag="humor")
        self.assertEqual(result, expected)
        mock_choice.assert_called_once()

    def test_get_random_quote_invalid_tag(self):
        with self.assertRaises(ValueError) as cm:
            get_random_quote(tag="nonexistent")
        self.assertIn("No quotes found for tag 'nonexistent'", str(cm.exception))


if __name__ == '__main__':
    unittest.main()
