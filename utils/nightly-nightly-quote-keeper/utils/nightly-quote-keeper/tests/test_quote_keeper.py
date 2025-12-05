import unittest
from unittest import mock

# Mock rationale: we patch ``random.choice`` to always return the first element of the provided sequence,
# guaranteeing deterministic behaviour without needing any external randomness.

from src.quote_keeper import get_random_quote, Quote


class TestQuoteKeeper(unittest.TestCase):
    def setUp(self):
        # Ensure ``random.choice`` is deterministic for all tests.
        self.choice_patcher = mock.patch(
            "src.quote_keeper.random.choice",
            side_effect=lambda seq: seq[0],
        )
        self.mock_choice = self.choice_patcher.start()
        self.addCleanup(self.choice_patcher.stop)

    def test_random_without_tag_returns_first_quote(self):
        quote = get_random_quote()
        self.assertIsInstance(quote, Quote)
        self.assertEqual(
            quote.text,
            "The only limit to our realization of tomorrow is our doubts of today.",
        )
        self.assertEqual(quote.author, "Franklin D. Roosevelt")

    def test_random_with_existing_tag_returns_correct_quote(self):
        quote = get_random_quote(tag="humor")
        self.assertEqual(quote.author, "Oscar Wilde")
        self.assertIn("humor", quote.tags)

    def test_random_with_unknown_tag_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            get_random_quote(tag="nonexistent")
        self.assertIn("No quotes found for tag", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
