import unittest
import datetime
from unittest.mock import patch

# Mock rationale: we replace ``datetime.date.today`` with a fixed date to make the test deterministic.
# This avoids any reliance on the actual current date or external state.

from utils.nightly-emoji-mood-meter.src.emoji_mood import get_mood_emoji

class TestEmojiMood(unittest.TestCase):
    def test_known_dates(self):
        # Mapping derived from the algorithm in ``emoji_mood.py``
        test_cases = [
            (datetime.date(2023, 1, 1), "🌅"),   # Day 1 -> index 0
            (datetime.date(2023, 1, 2), "😊"),   # Day 2 -> index 1
            (datetime.date(2023, 1, 12), "💤"),  # Day 12 -> index 11
            (datetime.date(2023, 1, 13), "🌅"),  # Cycle repeats
            (datetime.date(2024, 2, 29), "🤔"),  # Leap year day 60 -> index 4
        ]
        for dt, expected in test_cases:
            with self.subTest(date=dt):
                self.assertEqual(get_mood_emoji(dt), expected)

    @patch('utils.nightly-emoji-mood-meter.src.emoji_mood.datetime.date')
    def test_cli_output(self, mock_date):
        # Mock rationale: ensure the CLI prints the emoji for a known date.
        mock_date.today.return_value = datetime.date(2023, 3, 15)  # Day 74
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        from utils.nightly-emoji-mood-meter.src import emoji_mood
        # Capture stdout
        import io, sys
        captured = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = captured
        try:
            emoji_mood._cli()
        finally:
            sys.stdout = sys_stdout
        # Day 74 -> index (74-1)%12 = 1 -> "😊"
        self.assertEqual(captured.getvalue().strip(), "😊")

if __name__ == "__main__":
    unittest.main()
