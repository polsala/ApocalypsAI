import unittest
import os
import sys
import io
from contextlib import redirect_stdout

# Add the src directory to sys.path so we can import the module.
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from compliment import get_compliment, main

class TestCompliment(unittest.TestCase):
    def test_deterministic_output(self):
        first = get_compliment(seed=42)
        second = get_compliment(seed=42)
        self.assertEqual(first, second)

    def test_random_output_is_valid(self):
        result = get_compliment()
        self.assertIn(result, [
            "You're a coding wizard!",
            "Your mind is a treasure trove of ideas.",
            "You make the world brighter with your presence.",
            "Your curiosity fuels innovation.",
            "You have a knack for turning challenges into opportunities.",
            "Your smile is contagious.",
            "You bring clarity to complex problems.",
            "Your perseverance is inspiring.",
            "You have a brilliant sense of humor.",
            "Your kindness makes a difference."
        ])

    def test_cli_output(self):
        sys.argv = ["prog", "--seed", "42"]
        f = io.StringIO()
        with redirect_stdout(f):
            main()
        output = f.getvalue().strip()
        self.assertEqual(output, get_compliment(seed=42))

if __name__ == "__main__":
    unittest.main()
