import unittest
from src.quote_generator import get_quote, QUOTES


class TestQuoteGenerator(unittest.TestCase):
    def test_same_seed_repeatable(self):
        """Two calls with the same seed must yield the same quote.
        # Mock rationale: Using the deterministic ``random.Random`` ensures
        # repeatability without external services.
        """
        seed = 12345
        first = get_quote(seed=seed)
        second = get_quote(seed=seed)
        self.assertEqual(first, second)
        self.assertIn(first, QUOTES)

    def test_no_seed_returns_valid_quote(self):
        """Calling without a seed returns a string that is one of the known quotes.
        # Mock rationale: No network calls; relies solely on the in‑repo list.
        """
        quote = get_quote()
        self.assertIsInstance(quote, str)
        self.assertIn(quote, QUOTES)


if __name__ == "__main__":
    unittest.main()
