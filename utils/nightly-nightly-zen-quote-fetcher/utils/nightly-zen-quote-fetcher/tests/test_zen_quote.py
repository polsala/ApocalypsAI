import unittest
import io
import sys
from src.zen_quote import get_random_quote, main

class TestZenQuote(unittest.TestCase):
    def test_deterministic_selection(self):
        # Mock rationale: use a fixed seed to ensure deterministic choice.
        rng = __import__('random').Random(42)
        quote = get_random_quote(random_state=rng)
        # Expected quote based on seed 42 and the list order.
        self.assertEqual(quote, "Let go or be dragged.")  # Mock rationale: known outcome

    def test_main_prints_quote(self):
        # Mock rationale: capture stdout to verify output contains a known quote.
        captured = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = captured
        try:
            # Use deterministic RNG by monkeypatching get_random_quote
            original = get_random_quote
            def mock_get_random_quote(_=None):
                return "Simplicity is the ultimate sophistication."
            # Mock rationale: replace function to control output.
            globals()['get_random_quote'] = mock_get_random_quote
            main()
        finally:
            sys.stdout = sys_stdout
            globals()['get_random_quote'] = original
        output = captured.getvalue().strip()
        self.assertEqual(output, "Simplicity is the ultimate sophistication.")

if __name__ == '__main__':
    unittest.main()
