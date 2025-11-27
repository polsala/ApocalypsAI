import io
import sys
import unittest
from unittest import mock

# Import the module under test
from src.quote_generator import get_random_quote, main

class TestQuoteGenerator(unittest.TestCase):
    def test_deterministic_output_with_seed(self):
        # With a fixed seed, the quote should always be the same.
        seed = 42
        expected = "The wind whispers what the heart already knows."
        self.assertEqual(get_random_quote(seed=seed), expected)

    def test_output_is_one_of_the_known_quotes(self):
        quote = get_random_quote()
        from src.quote_generator import QUOTES
        self.assertIn(quote, QUOTES)

    @mock.patch('sys.argv', ['quote_generator', '--seed', '7'])
    def test_cli_prints_deterministic_quote(self):
        # Capture stdout
        captured = io.StringIO()
        # Mock rationale: redirect stdout to capture printed quote without affecting global state.
        with mock.patch('sys.stdout', new=captured):
            main()
        output = captured.getvalue().strip()
        # Seed 7 should produce a predictable quote.
        expected = "A single step is enough to begin the journey."
        self.assertEqual(output, expected)

if __name__ == "__main__":
    unittest.main()
