import unittest
from io import StringIO
import sys

# Mock rationale: Import the colourising function directly; no external I/O.
from src.main import colorize

class TestJsonPalette(unittest.TestCase):
    def test_simple_object(self):
        raw = '{"name": "Alice", "age": 30, "active": true, "spouse": null}'
        coloured = colorize(raw)
        # Expect ANSI colour codes for each type
        self.assertIn('\033[36m"name"\033[0m', coloured)   # key cyan
        self.assertIn('\033[32m"Alice"\033[0m', coloured)  # string green
        self.assertIn('\033[33m30\033[0m', coloured)        # number yellow
        self.assertIn('\033[35mtrue\033[0m', coloured)      # bool magenta
        self.assertIn('\033[31mnull\033[0m', coloured)      # null red

    def test_nested_structure(self):
        raw = '{"list": [1, "two", false], "obj": {"inner": null}}'
        coloured = colorize(raw)
        # Check a few nested colour codes
        self.assertIn('\033[36m"list"\033[0m', coloured)
        self.assertIn('\033[33m1\033[0m', coloured)
        self.assertIn('\033[32m"two"\033[0m', coloured)
        self.assertIn('\033[35mfalse\033[0m', coloured)
        self.assertIn('\033[36m"obj"\033[0m', coloured)
        self.assertIn('\033[31mnull\033[0m', coloured)

    def test_invalid_json_raises(self):
        raw = '{"unclosed": 123'
        with self.assertRaises(ValueError):
            colorize(raw)

if __name__ == '__main__':
    unittest.main()
