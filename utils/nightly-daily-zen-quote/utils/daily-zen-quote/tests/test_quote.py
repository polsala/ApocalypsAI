import io
import sys
import unittest
from unittest import mock

# Mock rationale: No external dependencies; deterministic behavior via seed.

from src.quote import get_quote, main

class TestDailyZenQuote(unittest.TestCase):
    def test_deterministic_with_seed(self):
        # Seed 1 should always return the first quote in the list
        quote = get_quote(seed=1)
        self.assertEqual(quote, "The journey of a thousand miles begins with one step.")

    def test_get_quote_returns_valid(self):
        quote = get_quote()
        self.assertIn(quote, [
            "The journey of a thousand miles begins with one step.",
            "When the mind is still, the universe surrenders.",
            "Simplicity is the ultimate sophistication.",
            "Let go or be dragged.",
            "The obstacle is the path.",
        ])

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_cli_output(self, mock_stdout):
        # Simulate CLI call with seed=1
        with mock.patch.object(sys, 'argv', ['daily-zen-quote', '--seed', '1']):
            exit_code = main()
        self.assertEqual(exit_code, 0)
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "The journey of a thousand miles begins with one step.")

if __name__ == '__main__':
    unittest.main()
