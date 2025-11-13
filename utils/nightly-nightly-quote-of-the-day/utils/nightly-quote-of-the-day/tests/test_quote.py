import unittest
from unittest.mock import patch

# Mock rationale: we patch ``random.choice`` to make the test deterministic without relying on actual randomness.

from src.quote import get_random_quote

class TestQuoteUtility(unittest.TestCase):
    def test_random_quote_without_category(self):
        # Force ``random.choice`` to return the first element of the list.
        with patch('random.choice', return_value=("The only limit to our realization of tomorrow is our doubts of today.", "Franklin D. Roosevelt", "motivation")):
            quote, author = get_random_quote()
            self.assertEqual(quote, "The only limit to our realization of tomorrow is our doubts of today.")
            self.assertEqual(author, "Franklin D. Roosevelt")

    def test_random_quote_with_category(self):
        # Patch to return a specific humor quote.
        with patch('random.choice', return_value=("Life is what happens when you're busy making other plans.", "John Lennon", "humor")):
            quote, author = get_random_quote(category="humor")
            self.assertEqual(quote, "Life is what happens when you're busy making other plans.")
            self.assertEqual(author, "John Lennon")

    def test_invalid_category_raises(self):
        with self.assertRaises(ValueError) as ctx:
            get_random_quote(category="nonexistent")
        self.assertIn("No quotes found for category", str(ctx.exception))

if __name__ == "__main__":
    unittest.main()
