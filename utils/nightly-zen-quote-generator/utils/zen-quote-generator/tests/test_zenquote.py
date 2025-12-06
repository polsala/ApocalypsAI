import io
import sys
import unittest
from unittest.mock import patch

# Mock rationale: Import the module from its relative path without side‑effects.
from src.zenquote import get_random_quote, main

class TestZenQuote(unittest.TestCase):
    def test_get_random_quote_mocked(self):
        """Ensure get_random_quote returns the mocked value.

        The test patches `random.choice` to return a deterministic quote,
        guaranteeing offline, repeatable behavior.
        """
        with patch('random.choice', return_value='Mocked Zen Quote'):
            self.assertEqual(get_random_quote(), 'Mocked Zen Quote')

    def test_cli_output_default(self):
        """Test the CLI prints the quote followed by a newline.

        `get_random_quote` is patched to a known value, and stdout is captured.
        """
        with patch('src.zenquote.get_random_quote', return_value='Test Quote'):
            captured = io.StringIO()
            sys_stdout_original = sys.stdout
            sys.stdout = captured
            try:
                main([])
            finally:
                sys.stdout = sys_stdout_original
            self.assertEqual(captured.getvalue(), 'Test Quote\n')

    def test_cli_output_no_newline(self):
        """Test the `--no-newline` flag suppresses the trailing newline.
        """
        with patch('src.zenquote.get_random_quote', return_value='No NL Quote'):
            captured = io.StringIO()
            sys_stdout_original = sys.stdout
            sys.stdout = captured
            try:
                main(['--no-newline'])
            finally:
                sys.stdout = sys_stdout_original
            self.assertEqual(captured.getvalue(), 'No NL Quote')

if __name__ == '__main__':
    unittest.main()
