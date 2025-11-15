import unittest
from unittest.mock import patch
import sys
import os
from io import StringIO

# Ensure the src directory is on the import path
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from compliment import get_compliment, main

class TestCompliment(unittest.TestCase):
    def test_get_compliment_specific_category(self):
        # Mock random.choice to return the first element
        with patch('random.choice', lambda seq: seq[0]):
            comp = get_compliment('coding')
            self.assertEqual(comp, "Your code is poetry in motion.")

    def test_get_compliment_unknown_category_uses_all(self):
        with patch('random.choice', lambda seq: seq[-1]):
            comp = get_compliment('unknown')
            # Last element of flattened list
            self.assertEqual(comp, "Every UI you touch becomes user-friendly.")

    def test_cli_output(self):
        test_args = ['prog', '--category', 'design']
        with patch.object(sys, 'argv', test_args):
            with patch('random.choice', lambda seq: seq[0]):
                captured = StringIO()
                sys_stdout = sys.stdout
                sys.stdout = captured
                try:
                    main()
                finally:
                    sys.stdout = sys_stdout
                self.assertEqual(captured.getvalue().strip(), "Your eye for design is impeccable.")

if __name__ == '__main__':
    unittest.main()
