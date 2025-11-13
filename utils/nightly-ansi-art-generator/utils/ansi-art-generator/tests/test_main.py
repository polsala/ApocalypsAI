import unittest
from unittest.mock import patch

# Mock rationale: we replace random.choice with a deterministic function so the output is predictable.

from ansi_art_generator.main import generate_art, BLOCK, RESET

class TestAnsiArtGenerator(unittest.TestCase):
    def test_generate_art_fixed_palette(self):
        # Deterministic palette of two colors
        palette = ["\u001b[31m", "\u001b[32m"]  # red, green
        # Mock random.choice to cycle through the palette in order
        def side_effect(_):
            # pop first element, append it back to simulate round‑robin
            color = palette.pop(0)
            palette.append(color)
            return color
        with patch('random.choice', side_effect=side_effect):
            art = generate_art(width=3, height=2, palette=["\u001b[31m", "\u001b[32m"])
        # Expected pattern: red, green, red on first line; green, red, green on second line
        expected = (
            f"\u001b[31m{BLOCK}{RESET}\u001b[32m{BLOCK}{RESET}\u001b[31m{BLOCK}{RESET}\n"
            f"\u001b[32m{BLOCK}{RESET}\u001b[31m{BLOCK}{RESET}\u001b[32m{BLOCK}{RESET}"
        )
        self.assertEqual(art, expected)

    def test_invalid_dimensions(self):
        with self.assertRaises(ValueError):
            generate_art(width=0, height=5)
        with self.assertRaises(ValueError):
            generate_art(width=5, height=-1)

if __name__ == "__main__":
    unittest.main()
