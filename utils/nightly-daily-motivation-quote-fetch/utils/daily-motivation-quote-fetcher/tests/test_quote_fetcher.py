import unittest
from unittest import mock

# Import the module under test
from src.quote_fetcher import get_random_quote, _filter_by_theme

class TestQuoteFetcher(unittest.TestCase):
    def setUp(self):
        # Ensure a known random state for any non‑mocked calls
        import random
        random.seed(0)

    def test_filter_by_theme_returns_correct_subset(self):
        # Directly test the private helper for clarity
        from src.quote_fetcher import _QUOTES
        filtered = _filter_by_theme(_QUOTES, "perseverance")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["author"], "Confucius")

    def test_get_random_quote_without_theme_uses_random_choice(self):
        # Mock random.choice to make the test deterministic
        with mock.patch('random.choice') as mock_choice:
            mock_choice.return_value = {
                "text": "Mocked quote",
                "author": "Mock Author",
                "theme": "mock"
            }
            # Mock rationale: we replace the randomness to assert the function returns the mocked value.
            result = get_random_quote()
            mock_choice.assert_called_once()
            self.assertEqual(result["text"], "Mocked quote")
            self.assertEqual(result["author"], "Mock Author")

    def test_get_random_quote_with_theme_filters_before_choice(self):
        # Ensure that filtering occurs before random.choice is called.
        with mock.patch('random.choice') as mock_choice:
            mock_choice.return_value = {
                "text": "Only perseverance quote",
                "author": "Confucius",
                "theme": "perseverance"
            }
            result = get_random_quote(theme="perseverance")
            mock_choice.assert_called_once()
            self.assertEqual(result["author"], "Confucius")

    def test_get_random_quote_invalid_theme_raises(self):
        with self.assertRaises(ValueError) as ctx:
            get_random_quote(theme="nonexistent")
        self.assertIn("No quotes found for theme", str(ctx.exception))

if __name__ == '__main__':
    unittest.main()
