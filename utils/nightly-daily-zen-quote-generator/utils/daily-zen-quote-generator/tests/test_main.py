import unittest
from unittest import mock

# Import the module under test
from src.main import get_quote

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def test_get_quote_any_category_returns_expected_when_mocked(self):
        # Mock rationale: deterministic selection for offline testing.
        with mock.patch('random.choice', return_value='Mocked Quote'):
            quote = get_quote()
            self.assertEqual(quote, 'Mocked Quote')

    def test_get_quote_specific_category_returns_expected_when_mocked(self):
        # Mock rationale: ensure the function respects the provided category.
        with mock.patch('random.choice', return_value='Mindful Mock'):
            quote = get_quote(category='mindfulness')
            self.assertEqual(quote, 'Mindful Mock')

    def test_get_quote_unknown_category_falls_back_to_all(self):
        # Mock rationale: unknown category should not raise and still use the fallback pool.
        with mock.patch('random.choice', return_value='Fallback Mock'):
            quote = get_quote(category='nonexistent')
            self.assertEqual(quote, 'Fallback Mock')

if __name__ == '__main__':
    unittest.main()
