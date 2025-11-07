import unittest
from unittest.mock import patch

# Import the function from the package's src directory.
from src.quote_generator import get_random_quote


class TestQuoteGenerator(unittest.TestCase):
    def test_random_quote_without_theme(self):
        """# Mock rationale: ensures deterministic test without randomness"""
        with patch('src.quote_generator.random.choice', return_value='Mocked Quote'):
            quote = get_random_quote()
            self.assertEqual(quote, 'Mocked Quote')

    def test_random_quote_with_valid_theme(self):
        """# Mock rationale: deterministic selection within theme pool"""
        with patch('src.quote_generator.random.choice', return_value='Theme Quote'):
            quote = get_random_quote(theme='mindfulness')
            self.assertEqual(quote, 'Theme Quote')

    def test_random_quote_with_invalid_theme_falls_back(self):
        """# Mock rationale: invalid theme should use full pool"""
        with patch('src.quote_generator.random.choice', return_value='Fallback Quote'):
            quote = get_random_quote(theme='nonexistent')
            self.assertEqual(quote, 'Fallback Quote')


if __name__ == '__main__':
    unittest.main()
