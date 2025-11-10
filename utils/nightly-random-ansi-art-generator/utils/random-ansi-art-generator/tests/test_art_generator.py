import unittest
from unittest.mock import patch

# Import from sibling src package
from src.art_generator import get_random_art, ART_COLLECTION

class TestRandomAnsiArtGenerator(unittest.TestCase):
    def test_get_random_art_deterministic(self):
        """Mock random.choice to ensure deterministic output."""
        expected = ART_COLLECTION[0]
        with patch('random.choice', return_value=expected):
            art = get_random_art()
        self.assertEqual(art, expected)

    def test_art_contains_ansi_codes(self):
        """Ensure the returned art includes at least one ANSI escape sequence."""
        art = get_random_art()
        self.assertIn("\033[", art)  # any ANSI code starts with ESC [

if __name__ == "__main__":
    unittest.main()
