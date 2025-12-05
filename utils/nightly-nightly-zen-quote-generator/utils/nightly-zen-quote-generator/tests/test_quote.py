import unittest
from unittest.mock import patch

# Mock rationale: We patch `random.choice` to return a deterministic value so the test does not rely on randomness.

from src.quote import get_random_quote, main

class TestZenQuoteGenerator(unittest.TestCase):
    def test_get_random_quote_deterministic(self):
        with patch('random.choice', return_value='Mocked Quote'):
            self.assertEqual(get_random_quote(), 'Mocked Quote')

    def test_cli_output(self):
        with patch('random.choice', return_value='CLI Mocked Quote'):
            # Capture stdout
            from io import StringIO
            import sys
            captured = StringIO()
            sys_stdout = sys.stdout
            sys.stdout = captured
            try:
                main()
            finally:
                sys.stdout = sys_stdout
            self.assertEqual(captured.getvalue().strip(), 'CLI Mocked Quote')

if __name__ == '__main__':
    unittest.main()
