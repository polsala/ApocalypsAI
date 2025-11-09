import unittest
from unittest.mock import patch
import sys
from io import StringIO

# Mock rationale: we patch random.choice to return a deterministic value so the test is offline and repeatable.

# Import the module under test
from utils.random_compliment_generator.src import main as compliment_module

class TestRandomComplimentGenerator(unittest.TestCase):
    def test_get_compliment_deterministic(self):
        # Force random.choice to return the first compliment
        with patch('random.choice', return_value=compliment_module.COMPLIMENTS[0]):
            self.assertEqual(
                compliment_module.get_compliment(),
                "You have the coding prowess of a caffeinated squirrel!"
            )

    def test_cli_output(self):
        # Capture stdout
        with patch('random.choice', return_value=compliment_module.COMPLIMENTS[1]):
            captured_out = StringIO()
            sys_stdout_original = sys.stdout
            sys.stdout = captured_out
            try:
                compliment_module.main()
            finally:
                sys.stdout = sys_stdout_original
            self.assertEqual(captured_out.getvalue().strip(), "Your debugging skills could tame a wild dragon.")

if __name__ == '__main__':
    unittest.main()
