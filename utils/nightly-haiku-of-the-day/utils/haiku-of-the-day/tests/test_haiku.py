import datetime
import os
import sys
import unittest

# Ensure the src directory is on the import path
CURRENT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "src"))
sys.path.append(SRC_DIR)

from haiku import generate_haiku

def _syllable(word: str) -> int:
    import re
    return len(re.findall(r"[aeiouy]+", word.lower()))

class TestHaikuOfTheDay(unittest.TestCase):
    def test_fixed_date_syllable_counts(self):
        """Verify that a known date yields lines with correct syllable counts."""
        date = datetime.date(2023, 1, 1)
        haiku = generate_haiku(date)
        lines = haiku.splitlines()
        self.assertEqual(len(lines), 3)
        self.assertEqual(sum(_syllable(w) for w in lines[0].split()), 5)
        self.assertEqual(sum(_syllable(w) for w in lines[1].split()), 7)
        self.assertEqual(sum(_syllable(w) for w in lines[2].split()), 5)

    def test_repeatability(self):
        """Same date must always produce the same haiku (determinism)."""
        date = datetime.date(2025, 12, 31)
        haiku1 = generate_haiku(date)
        haiku2 = generate_haiku(date)
        self.assertEqual(haiku1, haiku2)

    def test_today_is_string(self):
        """Calling without a date returns a string (no exception)."""
        haiku = generate_haiku()
        self.assertIsInstance(haiku, str)
        self.assertEqual(len(haiku.splitlines()), 3)

if __name__ == "__main__":
    unittest.main()
