import unittest
from unittest import mock
import sys
import io
import os

# Mock rationale: we set a deterministic seed so the random.choice outcome is predictable.
# This avoids flaky tests and keeps them offline.

# Ensure the src directory is on the import path
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "src"))
sys.path.insert(0, SRC_DIR)

from zen_quote import get_random_quote, main

class TestZenQuote(unittest.TestCase):
    def test_get_random_quote_deterministic(self):
        import random
        random.seed(42)
        quote = get_random_quote()
        # With seed 42, the chosen quote should always be the same from the list above.
        self.assertEqual(quote, "The journey of a thousand miles begins with one step.")

    def test_cli_output(self):
        test_args = ["zen_quote.py", "--seed", "123"]
        with mock.patch.object(sys, "argv", test_args):
            captured = io.StringIO()
            with mock.patch("sys.stdout", new=captured):
                main()
        output = captured.getvalue().strip().strip('"')
        # With seed 123, the expected quote is known.
        self.assertEqual(output, "Let go or be dragged.")

if __name__ == "__main__":
    unittest.main()
