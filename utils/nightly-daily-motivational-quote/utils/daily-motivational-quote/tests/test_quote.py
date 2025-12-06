import unittest
import sys
import os
from unittest.mock import patch

# Ensure the src directory is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from quote import get_random_quote

class TestQuote(unittest.TestCase):
    def test_random_quote_without_category(self):
        # Mock random.choice to return a deterministic quote
        with patch("quote.random.choice") as mock_choice:
            mock_choice.return_value = {
                "text": "Test quote",
                "author": "Tester",
                "category": "test",
            }
            result = get_random_quote()
            self.assertEqual(result, {"text": "Test quote", "author": "Tester"})
            mock_choice.assert_called_once()

    def test_random_quote_with_category(self):
        # Mock random.choice after filtering by category
        with patch("quote.random.choice") as mock_choice:
            mock_choice.return_value = {
                "text": "Life is what happens when you're busy making other plans.",
                "author": "John Lennon",
                "category": "life",
            }
            result = get_random_quote(category="life")
            self.assertEqual(
                result,
                {
                    "text": "Life is what happens when you're busy making other plans.",
                    "author": "John Lennon",
                },
            )
            mock_choice.assert_called_once()

    def test_invalid_category_raises(self):
        with self.assertRaises(ValueError) as cm:
            get_random_quote(category="nonexistent")
        self.assertIn("No quotes found for category", str(cm.exception))

if __name__ == "__main__":
    unittest.main()
