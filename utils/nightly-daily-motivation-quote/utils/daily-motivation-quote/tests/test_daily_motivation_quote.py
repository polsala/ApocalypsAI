import unittest
from src.daily_motivation_quote import get_random_quote, Quote

class TestDailyMotivationQuote(unittest.TestCase):
    def test_deterministic_output(self):
        # With a fixed seed we expect the same quote every run.
        quote1 = get_random_quote(seed=42)
        quote2 = get_random_quote(seed=42)
        self.assertEqual(quote1, quote2)
        # Verify the exact quote for this seed (based on the internal list).
        # Mock rationale: the seed 42 selects the third element in the shuffled order.
        self.assertEqual(quote1, "Take care of your body. It's the only place you have to live.")

    def test_category_filter(self):
        quote = get_random_quote(category="productivity", seed=1)
        # With seed=1 the deterministic choice from the two productivity quotes is known.
        # Mock rationale: seed 1 picks the first matching quote.
        self.assertIn(quote, [
            "The only way to do great work is to love what you do.",
            "Simplicity is the ultimate sophistication.",
        ])

    def test_invalid_category_raises(self):
        with self.assertRaises(ValueError) as ctx:
            get_random_quote(category="nonexistent")
        self.assertIn("No quotes found for category", str(ctx.exception))

if __name__ == "__main__":
    unittest.main()
