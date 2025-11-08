import unittest
from unittest.mock import patch

# Mock rationale: we replace random.choice to make the test deterministic.
# This ensures the utility works without any external randomness.

from src.compliment import get_random_compliment, main

class TestComplimentGenerator(unittest.TestCase):
    def test_get_random_compliment_deterministic(self):
        with patch('random.choice', return_value='You are a brilliant problem‑solver!'):
            self.assertEqual(get_random_compliment(), 'You are a brilliant problem‑solver!')

    def test_cli_output(self):
        with patch('random.choice', return_value='Your code reads like poetry.'):
            with patch('builtins.print') as mock_print:
                exit_code = main([])
                mock_print.assert_called_once_with('Your code reads like poetry.')
                self.assertEqual(exit_code, 0)

if __name__ == '__main__':
    unittest.main()
