import unittest
from unittest.mock import patch
import sys
import os
from io import StringIO

# Adjust sys.path to import the module from src
CURRENT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "src"))
sys.path.append(SRC_DIR)

from quote_dispenser import get_random_quote, main

class TestQuoteDispenser(unittest.TestCase):
    def test_get_random_quote_mocked(self):
        # Mock rationale: ensure deterministic output without randomness
        with patch('random.choice', return_value="Mocked Quote"):
            quote = get_random_quote()
            self.assertEqual(quote, "Mocked Quote")

    def test_cli_output(self):
        # Mock rationale: capture stdout and control random.choice
        with patch('random.choice', return_value="CLI Mocked Quote"):
            captured_out = StringIO()
            original_stdout = sys.stdout
            sys.stdout = captured_out
            try:
                main()
            finally:
                sys.stdout = original_stdout
            self.assertIn("CLI Mocked Quote", captured_out.getvalue().strip())

if __name__ == "__main__":
    unittest.main()
