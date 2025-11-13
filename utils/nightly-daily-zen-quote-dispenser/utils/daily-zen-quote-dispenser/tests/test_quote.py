import unittest
from unittest import mock

# Import the module under test
from utils.daily_zen_quote_dispenser.src.quote import get_random_quote, QUOTES

class TestQuoteUtility(unittest.TestCase):
    def test_deterministic_output_with_seed(self):
        # Using a fixed seed should always return the same quote
        quote1 = get_random_quote(seed=123)
        quote2 = get_random_quote(seed=123)
        self.assertEqual(quote1, quote2)
        # Ensure the quote is actually from the database
        self.assertIn(quote1, [q["text"] for q in QUOTES])

    def test_theme_filter_returns_correct_quote(self):
        # Choose a theme that we know exists
        quote = get_random_quote(theme="mindfulness", seed=0)
        self.assertIsNotNone(quote)
        # Verify the returned quote belongs to the requested theme
        matching_texts = [q["text"] for q in QUOTES if q["theme"] == "mindfulness"]
        self.assertIn(quote, matching_texts)

    def test_unknown_theme_returns_none(self):
        # Theme that does not exist should yield None
        result = get_random_quote(theme="nonexistent")
        self.assertIsNone(result)

    def test_random_choice_mocked(self):
        # Mock rationale: ensure deterministic output without relying on the random module.
        with mock.patch('random.choice', return_value=QUOTES[0]):
            quote = get_random_quote()
            self.assertEqual(quote, QUOTES[0]["text"])

if __name__ == "__main__":
    unittest.main()
