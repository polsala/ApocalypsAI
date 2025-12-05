import unittest
from datetime import datetime
from unittest.mock import patch

# Mock rationale: we import the function directly from the utility's source path.
# This keeps the test deterministic and offline.
from utils.nightly-emoji-mood-clock.src.emoji_clock import get_emoji_for_hour

class TestEmojiClock(unittest.TestCase):
    def test_valid_hour_mappings(self):
        # Exhaustive mapping based on the specification in README.
        expected = {
            0: "🌙", 1: "🌙", 2: "🌙", 3: "🌙", 4: "🌙", 5: "🌙",
            6: "🌅", 7: "🌅", 8: "🌅",
            9: "🌤️", 10: "🌤️", 11: "🌤️",
            12: "☀️", 13: "☀️",
            14: "🌞", 15: "🌞", 16: "🌞", 17: "🌞",
            18: "🌇", 19: "🌇",
            20: "🌌", 21: "🌌", 22: "🌌", 23: "🌌",
        }
        for hour, emoji in expected.items():
            with self.subTest(hour=hour):
                self.assertEqual(get_emoji_for_hour(hour), emoji)

    def test_invalid_hour_raises(self):
        for bad_hour in [-1, 24, 100]:
            with self.subTest(bad_hour=bad_hour):
                with self.assertRaises(ValueError):
                    get_emoji_for_hour(bad_hour)

    def test_cli_output_current_hour(self):
        # Mock datetime to a known hour and capture stdout.
        with patch('utils.nightly-emoji-mood-clock.src.emoji_clock.datetime') as mock_dt:
            mock_dt.datetime.now.return_value = datetime(2025, 12, 1, 14, 0, 0)
            mock_dt.datetime.now.return_value.hour = 14
            # Import the main function lazily to use the patched datetime.
            from utils.nightly-emoji-mood-clock.src.emoji_clock import main
            with patch('builtins.print') as mock_print:
                exit_code = main([])
                mock_print.assert_called_once_with("🌞")
                self.assertEqual(exit_code, 0)

if __name__ == "__main__":
    unittest.main()
