import unittest
import sys
from pathlib import Path
from datetime import date

# Mock rationale: add the package root to sys.path so the import works without installing.
sys.path.append(str(Path(__file__).resolve().parents[2]))  # utils/emoji-forecast

from src.forecast import get_emoji_for_date

class TestEmojiForecast(unittest.TestCase):
    def test_known_dates(self):
        # Mock rationale: using fixed dates to ensure deterministic output.
        cases = {
            date(1970, 1, 1): "☀️",   # 0 % 12 -> first emoji
            date(1970, 1, 2): "🌤️",   # 1 % 12 -> second emoji
            date(2025, 1, 1): "🌤️",   # 20089 days since epoch, 20089 % 12 == 1
        }
        for d, expected in cases.items():
            with self.subTest(d=d):
                self.assertEqual(get_emoji_for_date(d), expected)

if __name__ == "__main__":
    unittest.main()
