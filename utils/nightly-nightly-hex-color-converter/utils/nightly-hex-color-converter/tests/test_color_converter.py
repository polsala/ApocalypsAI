import unittest
from utils.nightly_hex_color_converter.src.color_converter import hex_to_rgb, rgb_to_hex

class TestColorConverter(unittest.TestCase):
    def test_hex_to_rgb_full(self):
        self.assertEqual(hex_to_rgb("#ff00aa"), (255, 0, 170))
        self.assertEqual(hex_to_rgb("ff00aa"), (255, 0, 170))

    def test_hex_to_rgb_short(self):
        # Short form #f0a expands to #ff00aa
        self.assertEqual(hex_to_rgb("#f0a"), (255, 0, 170))
        self.assertEqual(hex_to_rgb("f0a"), (255, 0, 170))

    def test_hex_to_rgb_invalid(self):
        with self.assertRaises(ValueError):
            hex_to_rgb("#gggggg")  # non‑hex characters
        with self.assertRaises(ValueError):
            hex_to_rgb("#1234")   # wrong length

    def test_rgb_to_hex(self):
        self.assertEqual(rgb_to_hex(255, 0, 170), "#ff00aa")
        self.assertEqual(rgb_to_hex(0, 0, 0), "#000000")
        self.assertEqual(rgb_to_hex(255, 255, 255), "#ffffff")

    def test_rgb_to_hex_invalid(self):
        # Mock rationale: ensure out‑of‑range values raise ValueError without external calls.
        with self.assertRaises(ValueError):
            rgb_to_hex(-1, 0, 0)
        with self.assertRaises(ValueError):
            rgb_to_hex(0, 256, 0)
        with self.assertRaises(ValueError):
            rgb_to_hex(300, 300, 300)

if __name__ == "__main__":
    unittest.main()
