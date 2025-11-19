import unittest
from unittest.mock import patch
from datetime import datetime

from src.mood_tracker import get_mood_emoji, main


class TestMoodEmoji(unittest.TestCase):
    def test_get_mood_emoji_valid_ranges(self):
        # Mock rationale: test each defined range deterministically
        cases = [
            (0, "🌙"),
            (5, "🌙"),
            (6, "🌅"),
            (9, "🌅"),
            (10, "☀️"),
            (13, "☀️"),
            (14, "🌤️"),
            (17, "🌤️"),
            (18, "🌇"),
            (20, "🌇"),
            (21, "🌙"),
            (23, "🌙"),
        ]
        for hour, expected in cases:
            with self.subTest(hour=hour):
                self.assertEqual(get_mood_emoji(hour), expected)

    def test_get_mood_emoji_invalid(self):
        # Mock rationale: ensure error handling for out‑of‑range values
        for hour in (-1, 24):
            with self.subTest(hour=hour):
                with self.assertRaises(ValueError):
                    get_mood_emoji(hour)

    @patch('src.mood_tracker.datetime')
    def test_cli_output(self, mock_datetime):
        # Mock rationale: control now() to a known hour
        mock_datetime.now.return_value = datetime(2023, 1, 1, 7, 30)
        # datetime.now().hour will be 7 -> 🌅
        with patch('builtins.print') as mock_print:
            main()
            mock_print.assert_called_once_with("🌅")


if __name__ == '__main__':
    unittest.main()
