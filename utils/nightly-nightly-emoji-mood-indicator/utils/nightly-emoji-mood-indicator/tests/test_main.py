import unittest
from unittest.mock import patch
import datetime

# Import the function from the utility package
from nightly_emoji_mood_indicator import get_mood_emoji

class TestMoodEmoji(unittest.TestCase):
    def test_morning(self):
        # Mock rationale: Provide a datetime at 06:30 UTC to represent morning.
        mock_dt = datetime.datetime(2023, 1, 1, 6, 30)
        self.assertEqual(get_mood_emoji(mock_dt), "🌅")

    def test_afternoon(self):
        # Mock rationale: Provide a datetime at 13:00 UTC to represent afternoon.
        mock_dt = datetime.datetime(2023, 1, 1, 13, 0)
        self.assertEqual(get_mood_emoji(mock_dt), "🌞")

    def test_evening(self):
        # Mock rationale: Provide a datetime at 19:45 UTC to represent evening.
        mock_dt = datetime.datetime(2023, 1, 1, 19, 45)
        self.assertEqual(get_mood_emoji(mock_dt), "🌇")

    def test_night_before_midnight(self):
        # Mock rationale: Provide a datetime at 22:15 UTC to represent night.
        mock_dt = datetime.datetime(2023, 1, 1, 22, 15)
        self.assertEqual(get_mood_emoji(mock_dt), "🌙")

    def test_night_after_midnight(self):
        # Mock rationale: Provide a datetime at 02:00 UTC to represent night.
        mock_dt = datetime.datetime(2023, 1, 2, 2, 0)
        self.assertEqual(get_mood_emoji(mock_dt), "🌙")

    @patch('nightly_emoji_mood_indicator.get_mood_emoji')
    def test_cli_output(self, mock_get):
        # Mock rationale: Ensure CLI prints the mocked emoji without invoking real time.
        mock_get.return_value = "🧪"
        with patch('builtins.print') as mock_print:
            from nightly_emoji_mood_indicator import main
            exit_code = main()
            mock_print.assert_called_once_with("🧪")
            self.assertEqual(exit_code, 0)

if __name__ == "__main__":
    unittest.main()
