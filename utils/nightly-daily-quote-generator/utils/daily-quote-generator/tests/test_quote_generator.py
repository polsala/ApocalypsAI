import datetime
import unittest
from unittest.mock import patch

# Import the module under test
from src.quote_generator import get_random_quote, get_quote_of_the_day

class TestQuoteGenerator(unittest.TestCase):
    def test_random_quote_fixed_seed(self):
        # Deterministic selection with a known seed
        quote = get_random_quote(seed=42)
        self.assertEqual(quote["text"], "I'm not arguing, I'm just explaining why I'm right.")
        self.assertEqual(quote["author"], "Anonymous")

    def test_random_quote_category_filter(self):
        # Seed + category should always return the same quote from that category
        quote = get_random_quote(seed=1, category="humor")
        self.assertEqual(quote["category"], "humor")
        self.assertEqual(quote["text"], "I have not failed. I've just found 10,000 ways that won't work.")
        # Mock rationale: the above expectation is based on the deterministic ordering of the filtered list.

    @patch('src.quote_generator.datetime.date')
    def test_quote_of_the_day_mock_date(self, mock_date):
        # Mock rationale: we replace datetime.date.today() to control the seed.
        mock_date.today.return_value = datetime.date(2023, 1, 1)
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        quote = get_quote_of_the_day()
        # Seed derived from 20230101 should pick a specific quote
        self.assertEqual(quote["text"], "Life is what happens when you're busy making other plans.")
        self.assertEqual(quote["author"], "John Lennon")

if __name__ == "__main__":
    unittest.main()
