import unittest
from unittest import mock

# Mock rationale: patching ``random.choice`` guarantees deterministic output without network.
from src.quote_generator import get_random_quote, QUOTES

class TestQuoteGenerator(unittest.TestCase):
    def test_random_quote_all_categories(self):
        # Prepare a deterministic return value
        expected = ("The only true wisdom is in knowing you know nothing.", "Socrates")
        with mock.patch('random.choice', return_value=expected) as mock_choice:
            quote, author = get_random_quote()
            mock_choice.assert_called_once()
            self.assertEqual((quote, author), expected)

    def test_random_quote_specific_category(self):
        expected = ("I can resist everything except temptation.", "Oscar Wilde")
        with mock.patch('random.choice', return_value=expected) as mock_choice:
            quote, author = get_random_quote(category="humor")
            mock_choice.assert_called_once()
            self.assertEqual((quote, author), expected)

    def test_invalid_category_raises(self):
        with self.assertRaises(ValueError) as cm:
            get_random_quote(category="nonexistent")
        self.assertIn("Unknown category", str(cm.exception))

if __name__ == "__main__":
    unittest.main()
