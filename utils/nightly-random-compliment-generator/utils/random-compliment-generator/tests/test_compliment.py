import unittest
import importlib.util
import pathlib
from unittest.mock import patch


def load_module():
    # Resolve the path to the module two directories up from this test file
    path = pathlib.Path(__file__).resolve().parents[2] / "src" / "compliment.py"
    spec = importlib.util.spec_from_file_location("compliment", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestComplimentGenerator(unittest.TestCase):
    def setUp(self):
        self.mod = load_module()

    def test_general_category(self):
        # Mock random.choice to always return the first element of the sequence
        with patch('random.choice', lambda seq: seq[0]):
            result = self.mod.get_compliment('general')
            self.assertEqual(result, "You're a fantastic problem‑solver!")

    def test_unknown_category_falls_back_to_all(self):
        # Mock random.choice to return the last element of the flattened list
        with patch('random.choice', lambda seq: seq[-1]):
            result = self.mod.get_compliment('nonexistent')
            self.assertEqual(result, "You debug with the precision of a surgeon.")

    def test_no_category_random(self):
        # Mock random.choice to return the 4th element (index 3) of the flattened list
        with patch('random.choice', lambda seq: seq[3]):
            result = self.mod.get_compliment()
            self.assertEqual(result, "Your imagination paints the sky with new colors.")


if __name__ == '__main__':
    unittest.main()
