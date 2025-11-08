import unittest
from src.main import generate_art

class TestRandomAnsiArtGenerator(unittest.TestCase):
    def test_deterministic_output(self):
        # Mock rationale: generate_art is pure; no external dependencies.
        art1 = generate_art(3, 2, seed=42)
        art2 = generate_art(3, 2, seed=42)
        self.assertEqual(art1, art2)

    def test_known_output(self):
        # With seed 0, width 2, height 1, we know the exact ANSI sequence.
        expected = "\x1b[31;44m█\x1b[0m\x1b[33;45m█\x1b[0m"
        art = generate_art(2, 1, seed=0)
        self.assertEqual(art, expected)

    def test_invalid_dimensions(self):
        with self.assertRaises(ValueError):
            generate_art(0, 5)
        with self.assertRaises(ValueError):
            generate_art(5, -1)

if __name__ == "__main__":
    unittest.main()
