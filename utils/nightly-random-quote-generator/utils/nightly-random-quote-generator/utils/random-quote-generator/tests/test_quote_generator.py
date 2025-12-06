import unittest
from unittest import mock

# Mock rationale: all randomness is mocked to guarantee deterministic outcomes.
from src.quote_generator import get_random_quote

class TestQuoteGenerator(unittest.TestCase):
    def test_random_quote_no_category(self):
        with mock.patch('random.choice', return_value='Mocked Quote') as mock_choice:
            result = get_random_quote()
            mock_choice.assert_called_once()
            self.assertEqual(result, 'Mocked Quote')

    def test_random_quote_with_category(self):
        # Ensure only quotes from the specified category are considered.
        with mock.patch('random.choice', side_effect=lambda seq: seq[0]) as mock_choice:
            result = get_random_quote(category='humor')
            # The first humor quote in the static list is:
            expected = "The early bird gets the worm, but the second mouse gets the cheese."
            self.assertEqual(result, expected)
            # Verify that random.choice received a list containing only humor quotes.
            args_passed = mock_choice.call_args[0][0]
            self.assertTrue(all('humor' in q for q in args_passed))

    def test_invalid_category_raises(self):
        with self.assertRaises(ValueError) as cm:
            get_random_quote(category='nonexistent')
        self.assertIn("No quotes found for category 'nonexistent'", str(cm.exception))

if __name__ == '__main__':
    unittest.main()
