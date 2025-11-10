import os
import sys
import random
import unittest

# Adjust path to import the src module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from main import get_quote

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def setUp(self):
        # Ensure deterministic randomness for each test
        random.seed(0)

    def test_random_quote_deterministic(self):
        quote = get_quote()
        # With seed 0, the first random.choice from the full list yields this quote:
        expected = "The journey of a thousand miles begins with one step."
        self.assertEqual(quote, expected)

    def test_tag_filter(self):
        random.seed(1)
        quote = get_quote(tag="humor")
        # With seed 1 and humor tag, expected quote:
        expected = "If you cannot find the truth within yourself, look elsewhere."
        self.assertEqual(quote, expected)

    def test_invalid_tag(self):
        with self.assertRaises(ValueError) as ctx:
            get_quote(tag="nonexistent")
        self.assertIn("No quotes found for tag", str(ctx.exception))

if __name__ == "__main__":
    unittest.main()
