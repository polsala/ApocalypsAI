import unittest
from utils.hex-color-converter.src.converter import hex_to_rgb, rgb_to_hex

class TestHexColorConverter(unittest.TestCase):
    def test_hex_to_rgb_valid(self):
        self.assertEqual(hex_to_rgb("#ff00aa"), (255, 0, 170))
        self.assertEqual(hex_to_rgb("ff00aa"), (255, 0, 170))
        self.assertEqual(hex_to_rgb("#1E90FF"), (30, 144, 255))

    def test_hex_to_rgb_invalid(self):
        with self.assertRaises(ValueError):
            hex_to_rgb("#gggggg")  # non‑hex characters
        with self.assertRaises(ValueError):
            hex_to_rgb("12345")   # wrong length
        with self.assertRaises(ValueError):
            hex_to_rgb("#1234567")  # too long

    def test_rgb_to_hex_valid(self):
        self.assertEqual(rgb_to_hex((255, 0, 170)), "#ff00aa")
        self.assertEqual(rgb_to_hex((30, 144, 255)), "#1e90ff")
        self.assertEqual(rgb_to_hex((0, 0, 0)), "#000000")
        self.assertEqual(rgb_to_hex((255, 255, 255)), "#ffffff")

    def test_rgb_to_hex_invalid(self):
        with self.assertRaises(ValueError):
            rgb_to_hex((-1, 0, 0))   # negative component
        with self.assertRaises(ValueError):
            rgb_to_hex((256, 0, 0))  # component >255
        with self.assertRaises(ValueError):
            rgb_to_hex((0, 0))       # wrong tuple size – will raise TypeError before validation

if __name__ == "__main__":
    unittest.main()
