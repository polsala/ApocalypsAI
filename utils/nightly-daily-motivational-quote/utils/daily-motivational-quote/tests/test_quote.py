import unittest
from unittest.mock import patch
import sys
import os

# Add src directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from quote import get_random_quote, format_quote, main

class TestQuoteUtility(unittest.TestCase):
    def test_get_random_quote_mock(self):
        # Mock random.choice to always return the first quote
        # Mock rationale: Ensure deterministic output without randomness.
        with patch('quote.random.choice') as mock_choice:
            mock_choice.return_value = ("Believe you can and you're halfway there.", "Theodore Roosevelt")
            quote, author = get_random_quote()
            self.assertEqual(quote, "Believe you can and you're halfway there.")
            self.assertEqual(author, "Theodore Roosevelt")

    def test_format_quote(self):
        formatted = format_quote("Stay hungry, stay foolish.", "Steve Jobs")
        self.assertEqual(formatted, '"Stay hungry, stay foolish." – Steve Jobs')

    def test_main_output(self):
        # Capture stdout
        # Mock rationale: Verify CLI prints the correctly formatted quote.
        with patch('quote.random.choice') as mock_choice, \
             patch('sys.stdout') as mock_stdout:
            mock_choice.return_value = ("You miss 100% of the shots you don’t take.", "Wayne Gretzky")
            from io import StringIO
            mock_stdout.write = StringIO().write
            main()
            output = mock_stdout.write.call_args[0][0]
            expected = '"You miss 100% of the shots you don’t take." – Wayne Gretzky\n'
            self.assertEqual(output, expected)

if __name__ == '__main__':
    unittest.main()
