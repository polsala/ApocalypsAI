import unittest
from unittest import mock

# Import the module under test.
from src.main import get_random_quote, _filter_quotes

class TestDailyMotivationQuote(unittest.TestCase):
    def test_filter_all(self):
        # No category → all quotes returned.
        all_quotes = _filter_quotes(None)
        self.assertEqual(len(all_quotes), 6)

    def test_filter_specific(self):
        humor = _filter_quotes("humor")
        self.assertTrue(all(q["category"] == "humor" for q in humor))
        self.assertEqual(len(humor), 2)

    def test_filter_case_insensitive(self):
        insp = _filter_quotes("InSpIrAtIoN")
        self.assertEqual(len(insp), 2)
        self.assertTrue(all(q["category"] == "inspiration" for q in insp))

    def test_get_random_quote_deterministic(self):
        # Mock ``random.choice`` to always return the first element.
        with mock.patch('random.choice', side_effect=lambda seq: seq[0]):
            quote = get_random_quote()
            # The first quote in the static list.
            self.assertEqual(quote, "Believe you can and you're halfway there.")

    def test_get_random_quote_with_category(self):
        with mock.patch('random.choice', side_effect=lambda seq: seq[0]):
            quote = get_random_quote('humor')
            self.assertEqual(quote, "I am not lazy, I am on energy‑saving mode.")

    def test_get_random_quote_invalid_category(self):
        with self.assertRaises(ValueError) as ctx:
            get_random_quote('nonexistent')
        self.assertIn("No quotes found for category 'nonexistent'", str(ctx.exception))

if __name__ == '__main__':
    unittest.main()
