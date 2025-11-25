import builtins
import sys
from unittest import mock
import unittest

# Mock rationale: we replace ``random.choice`` with a deterministic function so the test is repeatable offline.

from src.quote_generator import get_random_quote, main

class TestQuoteGenerator(unittest.TestCase):
    def test_get_random_quote_deterministic(self):
        with mock.patch('random.choice', return_value='Mocked Zen Quote'):
            self.assertEqual(get_random_quote(), 'Mocked Zen Quote')

    def test_cli_outputs_mocked_quote(self):
        # Patch ``random.choice`` and capture stdout.
        with mock.patch('random.choice', return_value='CLI Mock Quote'):
            with mock.patch.object(sys, 'stdout', new_callable=mock.MagicMock) as fake_out:
                exit_code = main([])
                # ``print`` adds a newline; capture the first call argument.
                fake_out.write.assert_called_once_with('CLI Mock Quote\n')
                self.assertEqual(exit_code, 0)

if __name__ == '__main__':
    unittest.main()
