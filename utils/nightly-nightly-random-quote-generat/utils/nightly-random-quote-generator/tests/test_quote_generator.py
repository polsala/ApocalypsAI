import unittest
from unittest.mock import patch

from src.quote_generator import get_random_quote, format_quote


class TestQuoteGenerator(unittest.TestCase):
    def test_get_random_quote_no_tag(self):
        # Mock rationale: deterministic selection for test stability.
        with patch('src.quote_generator.random.choice') as mock_choice:
            mock_choice.side_effect = lambda seq: seq[0]
            quote = get_random_quote()
            self.assertEqual(
                quote["text"],
                "The early bird gets the worm, but the second mouse gets the cheese.",
            )

    def test_get_random_quote_with_tag(self):
        # Mock rationale: deterministic selection for test stability.
        with patch('src.quote_generator.random.choice') as mock_choice:
            mock_choice.side_effect = lambda seq: seq[-1]
            quote = get_random_quote(tag="inspiration")
            # Two quotes have the 'inspiration' tag; we expect the last one.
            self.assertIn(
                quote["text"],
                [
                    "Dreams are the seedlings of reality.",
                    "Stars can't shine without darkness.",
                ],
            )

    def test_get_random_quote_invalid_tag(self):
        with self.assertRaises(ValueError):
            get_random_quote(tag="nonexistent")

    def test_format_quote_text(self):
        quote = {"text": "Sample quote", "tags": []}
        self.assertEqual(format_quote(quote, fmt="text"), "Sample quote")

    def test_format_quote_json(self):
        quote = {"text": "Sample quote", "tags": []}
        self.assertEqual(format_quote(quote, fmt="json"), '{"text": "Sample quote", "tags": []}')


if __name__ == "__main__":
    unittest.main()
