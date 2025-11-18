import io
import sys
import unittest
from unittest.mock import patch

# Import the module under test
from utils.nightly-motivational-quote-dispenser.src.quote_dispenser import (
    get_random_quote,
    main,
)

class TestQuoteDispenser(unittest.TestCase):
    def test_get_random_quote_deterministic(self):
        """# Mock rationale: Ensure deterministic output by mocking random.choice.
        We patch `random.choice` to always return the first element of the list.
        """
        with patch('random.choice', return_value='MOCKED QUOTE'):
            self.assertEqual(get_random_quote(), 'MOCKED QUOTE')

    def test_cli_output(self):
        """# Mock rationale: Capture stdout while mocking the random choice to a known value.
        This guarantees the CLI prints the expected quoted string.
        """
        with patch('random.choice', return_value='CLI MOCKED QUOTE'):
            captured = io.StringIO()
            sys_stdout_original = sys.stdout
            sys.stdout = captured
            try:
                main()
            finally:
                sys.stdout = sys_stdout_original
            output = captured.getvalue().strip()
            self.assertEqual(output, '"CLI MOCKED QUOTE"')

if __name__ == '__main__':
    unittest.main()
