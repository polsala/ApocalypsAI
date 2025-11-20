import unittest
from unittest import mock
from src.quote import get_quotes, pick_random, format_quote

class TestQuoteUtility(unittest.TestCase):
    def test_get_quotes_all(self):
        all_quotes = get_quotes()
        self.assertGreaterEqual(len(all_quotes), 5)

    def test_get_quotes_category(self):
        insp = get_quotes("inspiration")
        self.assertTrue(all(q[2] == "inspiration" for q in insp))
        self.assertEqual(len(insp), 1)

    def test_get_quotes_invalid_category(self):
        none = get_quotes("nonexistent")
        self.assertEqual(none, [])

    @mock.patch("random.choice")
    def test_pick_random_mock(self, mock_choice):
        # Mock rationale: deterministic selection for test stability
        mock_choice.return_value = ("Test quote", "Tester", "test")
        quote = pick_random([("Test quote", "Tester", "test")])
        mock_choice.assert_called_once()
        self.assertEqual(quote, ("Test quote", "Tester", "test"))

    def test_format_quote(self):
        formatted = format_quote(("Hello world", "Alice", "test"))
        self.assertEqual(formatted, '"Hello world" — Alice')

if __name__ == "__main__":
    unittest.main()
