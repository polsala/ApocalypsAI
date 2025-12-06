import unittest
from unittest.mock import patch
from src.zen import get_random_quote, format_quote

class TestZen(unittest.TestCase):
    @patch('src.zen.random.choice')
    def test_get_random_quote_mock(self, mock_choice):
        # Mock rationale: ensure deterministic output without randomness
        mock_choice.return_value = "Mocked quote"
        self.assertEqual(get_random_quote(), "Mocked quote")
        mock_choice.assert_called_once_with([
            "The journey of a thousand miles begins with one step.",
            "Simplicity is the ultimate sophistication.",
            "When the mind is still, the universe surrenders.",
            "Let go or be dragged.",
            "The obstacle is the path."
        ])

    def test_format_quote_without_art(self):
        quote = "Test quote"
        self.assertEqual(format_quote(quote, art=False), "Test quote")

    def test_format_quote_with_art(self):
        quote = "Test quote"
        result = format_quote(quote, art=True)
        self.assertTrue(result.startswith("      __"))
        self.assertIn(quote, result)

if __name__ == '__main__':
    unittest.main()
