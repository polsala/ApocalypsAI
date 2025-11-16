import unittest
import sys
import os

# Add the src directory to ``sys.path`` so the module can be imported.
# Mock rationale: we need a deterministic import path without relying on
# external packaging tools.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from hex_color_namer import hex_to_name, _parse_hex

class TestHexColorNamer(unittest.TestCase):
    def test_basic_colors(self):
        self.assertEqual(hex_to_name("#000000"), "black")
        self.assertEqual(hex_to_name("#FFFFFF"), "white")
        self.assertEqual(hex_to_name("#FF0000"), "red")
        self.assertEqual(hex_to_name("#00FF00"), "lime")
        self.assertEqual(hex_to_name("#0000FF"), "blue")

    def test_nearest_match(self):
        # A shade of orange is closer to red than to any other palette entry.
        self.assertEqual(hex_to_name("#FF4500"), "red")
        # A tealish colour should resolve to teal.
        self.assertEqual(hex_to_name("#008080"), "teal")

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            _parse_hex("not-a-hex")
        with self.assertRaises(ValueError):
            _parse_hex("#123AB")  # only 5 digits

if __name__ == "__main__":
    unittest.main()
