import unittest
from unittest.mock import patch

from src.quote_generator import QuoteGenerator, Quote


class TestQuoteGenerator(unittest.TestCase):
    def setUp(self) -> None:
        self.generator = QuoteGenerator()

    def test_random_quote_without_theme(self):
        # Mock random.choice to return a known quote
        mock_quote = Quote(text="Mocked quote", theme="mock")
        with patch('random.choice', return_value=mock_quote) as mock_choice:  # Mock rationale: deterministic test
            result = self.generator.get_random_quote()
            mock_choice.assert_called_once()
            self.assertEqual(result, mock_quote)

    def test_random_quote_with_valid_theme(self):
        # Ensure filtering works and mock the choice within the filtered list
        theme = "growth"
        eligible = [q for q in self.generator._quotes if q.theme == theme]
        mock_quote = eligible[0]
        with patch('random.choice', return_value=mock_quote) as mock_choice:  # Mock rationale: deterministic test
            result = self.generator.get_random_quote(theme=theme)
            mock_choice.assert_called_once_with(eligible)
            self.assertEqual(result, mock_quote)

    def test_random_quote_with_invalid_theme_raises(self):
        with self.assertRaises(ValueError) as cm:
            self.generator.get_random_quote(theme="nonexistent")
        self.assertIn("No quotes found for theme 'nonexistent'", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
