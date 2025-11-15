import datetime
import unittest
from src.haiku import generate, FIVE_SYLLABLE_LINES, SEVEN_SYLLABLE_LINES

class TestHaikuGenerator(unittest.TestCase):
    def test_three_lines(self):
        # Mock rationale: Ensure the output always contains exactly three lines.
        haiku = generate(datetime.date(2022, 6, 15))
        self.assertEqual(len(haiku.splitlines()), 3)

    def test_consistency_same_date(self):
        # Mock rationale: Same date should always produce the same haiku.
        test_date = datetime.date(2025, 12, 25)
        haiku1 = generate(test_date)
        haiku2 = generate(test_date)
        self.assertEqual(haiku1, haiku2)

    def test_lines_are_from_wordbanks(self):
        # Mock rationale: Verify each line originates from the predefined word banks.
        haiku = generate(datetime.date(2023, 3, 14))
        line1, line2, line3 = haiku.splitlines()
        self.assertIn(line1, FIVE_SYLLABLE_LINES)
        self.assertIn(line2, SEVEN_SYLLABLE_LINES)
        self.assertIn(line3, FIVE_SYLLABLE_LINES)

if __name__ == "__main__":
    unittest.main()
