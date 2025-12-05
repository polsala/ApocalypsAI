import unittest
from unittest.mock import patch
import datetime
from src.mood_meter import get_mood

class TestMoodMeter(unittest.TestCase):
    def test_explicit_hours(self):
        """Check that each defined hour range returns the correct emoji."""
        cases = {
            2: "🌙",
            7: "🌅",
            11: "☕",
            15: "💼",
            19: "🌆",
            22: "🌙",
        }
        for hour, expected in cases.items():
            with self.subTest(hour=hour):
                self.assertEqual(get_mood(hour), expected)

    def test_current_hour_mock(self):
        """# Mock rationale: ensure deterministic hour without real time"""
        mock_now = datetime.datetime(2025, 1, 1, 9, 0, 0)
        with patch("src.mood_meter.datetime") as mock_dt:
            mock_dt.datetime.now.return_value = mock_now
            mock_dt.datetime.now.return_value.hour = 9
            self.assertEqual(get_mood(), "🌅")

    def test_invalid_hour(self):
        for invalid in (-5, 24, 100):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    get_mood(invalid)

if __name__ == "__main__":
    unittest.main()
