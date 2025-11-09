import unittest
from src.quote_generator import get_random_quote

class TestQuoteGenerator(unittest.TestCase):
    def test_random_quote_deterministic(self):
        # Using a fixed seed should always return the same quote.
        quote = get_random_quote(seed=42)
        self.assertEqual(
            quote,
            "The early bird gets the worm, but the second mouse gets the cheese.",
        )

    def test_category_filter_humor(self):
        # Seed ensures deterministic selection within the filtered list.
        quote = get_random_quote(category="humor", seed=1)
        self.assertIn(quote, [
            "The early bird gets the worm, but the second mouse gets the cheese.",
            "When life gives you lemons, make lemonade. Then find someone whose life gave them vodka, and have a party.",
        ])

    def test_invalid_category_raises(self):
        with self.assertRaises(ValueError) as cm:
            get_random_quote(category="nonexistent")
        self.assertEqual(str(cm.exception), "No quotes found for category 'nonexistent'.")

if __name__ == "__main__":
    unittest.main()
