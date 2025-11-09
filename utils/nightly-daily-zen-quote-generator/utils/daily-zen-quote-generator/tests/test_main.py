import os
import sys
import unittest
from unittest.mock import patch

# Ensure the src directory is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from src.main import get_random_quote, main

class TestQuoteGenerator(unittest.TestCase):
    def test_get_random_quote_no_tag(self):
        # Mock random.choice to return the first element deterministically
        with patch('random.choice', lambda seq: seq[0]):
            quote = get_random_quote()
            self.assertEqual(
                quote,
                "The journey of a thousand miles begins with one step."
            )

    def test_get_random_quote_with_tag(self):
        with patch('random.choice', lambda seq: seq[0]):
            quote = get_random_quote(tag="mindfulness")
            self.assertEqual(
                quote,
                "When the mind is still, the universe surrenders."
            )

    def test_get_random_quote_invalid_tag(self):
        with self.assertRaises(ValueError) as cm:
            get_random_quote(tag="nonexistent")
        self.assertIn("No quotes found for tag", str(cm.exception))

    def test_cli_success(self):
        test_argv = ["prog", "--tag", "zen"]
        with patch('random.choice', lambda seq: seq[0]), \
             patch.object(sys, 'argv', test_argv), \
             patch('builtins.print') as mock_print:
            exit_code = main()
            self.assertEqual(exit_code, 0)
            mock_print.assert_called_once_with(
                "The journey of a thousand miles begins with one step."
            )

    def test_cli_invalid_tag(self):
        test_argv = ["prog", "--tag", "unknown"]
        with patch('random.choice', lambda seq: seq[0]), \
             patch.object(sys, 'argv', test_argv), \
             patch('builtins.print') as mock_print:
            exit_code = main()
            self.assertEqual(exit_code, 1)
            # Ensure an error message was printed to stderr (captured via mock)
            mock_print.assert_called()

if __name__ == '__main__':
    unittest.main()
