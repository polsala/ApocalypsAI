import unittest
from src.quote import get_quote

class TestDailyZenQuote(unittest.TestCase):
    def test_deterministic_consistency(self):
        """Two calls with the same seed must return the same quote."""
        seed = 12345
        first = get_quote(seed)
        second = get_quote(seed)
        self.assertEqual(first, second)

    def test_returns_string(self):
        """Without a seed the function should still return a non‑empty string.
        # Mock rationale: no external dependencies, pure function.
        """
        quote = get_quote()
        self.assertIsInstance(quote, str)
        self.assertTrue(len(quote) > 0)

if __name__ == "__main__":
    unittest.main()
