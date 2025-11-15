import unittest
from unittest.mock import patch

# Mock rationale: we patch `random.choice` to return a deterministic quote,
# ensuring the test runs offline and produces a predictable result.

from utils.daily-zen-quote-dispenser.src.zen import get_random_quote, Quote


class TestZenQuoteDispenser(unittest.TestCase):
    def setUp(self):
        # A known quote from the pool for deterministic comparison
        self.sample_quote = Quote(
            text="The journey of a thousand miles begins with a single step.",
            tags=["mindfulness", "motivation"],
        )

    @patch("random.choice", return_value=Quote(
        text="The journey of a thousand miles begins with a single step.",
        tags=["mindfulness", "motivation"],
    ))
    def test_get_random_quote_no_tag(self, mock_choice):
        quote = get_random_quote()
        self.assertEqual(quote, self.sample_quote)
        mock_choice.assert_called_once()

    @patch("random.choice", return_value=Quote(
        text="A cup of tea is a cup of peace.",
        tags=["humor", "mindfulness"],
    ))
    def test_get_random_quote_with_tag(self, mock_choice):
        quote = get_random_quote(tag="humor")
        self.assertEqual(quote.text, "A cup of tea is a cup of peace.")
        self.assertIn("humor", quote.tags)
        mock_choice.assert_called_once()

    def test_get_random_quote_invalid_tag(self):
        with self.assertRaises(ValueError) as cm:
            get_random_quote(tag="nonexistent")
        self.assertIn("No quotes found for tag", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
