import unittest
import sys
import os
from unittest.mock import patch

# Ensure the src directory is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from main import get_quote


class TestDailyZenQuoteGenerator(unittest.TestCase):
    def test_get_quote_no_theme(self):
        # Mock random.choice to return the first quote
        with patch('random.choice', return_value={"text": "The journey of a thousand miles begins with one step.", "theme": "journey"}):
            quote = get_quote()
            self.assertEqual(quote, "The journey of a thousand miles begins with one step.")

    def test_get_quote_with_theme(self):
        # Mock random.choice to return the matching quote
        with patch('random.choice', return_value={"text": "Silence is a source of great strength.", "theme": "silence"}):
            quote = get_quote(theme="silence")
            self.assertEqual(quote, "Silence is a source of great strength.")

    def test_get_quote_invalid_theme(self):
        with self.assertRaises(ValueError) as cm:
            get_quote(theme="nonexistent")
        self.assertIn("No quotes found for theme", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
