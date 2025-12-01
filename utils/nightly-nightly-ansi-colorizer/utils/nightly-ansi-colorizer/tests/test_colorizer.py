import unittest
from ansi_colorizer import colorize

class TestAnsiColorizer(unittest.TestCase):
    def test_no_style_returns_original(self):
        self.assertEqual(colorize("plain"), "plain")

    def test_single_color(self):
        # red foreground = 31
        expected = "\x1b[31mHello\x1b[0m"
        self.assertEqual(colorize("Hello", "red"), expected)

    def test_multiple_styles_order(self):
        # bold (1) + blue (34) => "1;34"
        expected = "\x1b[1;34mWorld\x1b[0m"
        self.assertEqual(colorize("World", "bold", "blue"), expected)

    def test_unknown_style_is_ignored(self):
        # Mock rationale: we want deterministic behavior without external I/O.
        # The function prints a warning to stderr for unknown styles; we ignore that output.
        expected = "\x1b[32mTest\x1b[0m"  # green = 32
        self.assertEqual(colorize("Test", "green", "nonexistent"), expected)

    def test_bright_color_and_attribute(self):
        # bright_yellow (93) + underline (4)
        expected = "\x1b[93;4mShiny\x1b[0m"
        self.assertEqual(colorize("Shiny", "bright_yellow", "underline"), expected)

if __name__ == "__main__":
    unittest.main()
