import unittest
from unittest.mock import patch
from pathlib import Path
import datetime
import sys

# Ensure src is importable relative to this test file
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.logger import log_mood, format_entry, get_mood_emoji, MOOD_EMOJIS

class TestEmojiMoodLogger(unittest.TestCase):
    def setUp(self):
        # Use a temporary file for each test
        self.test_log = Path("test_mood.log")
        if self.test_log.exists():
            self.test_log.unlink()

    def tearDown(self):
        if self.test_log.exists():
            self.test_log.unlink()

    @patch("src.logger.random.choice")
    def test_get_mood_emoji_mock(self, mock_choice):
        # Mock rationale: deterministic emoji for test
        mock_choice.return_value = "🤩"
        emoji = get_mood_emoji()
        self.assertEqual(emoji, "🤩")
        mock_choice.assert_called_once_with(MOOD_EMOJIS)

    @patch("src.logger.random.choice")
    @patch("src.logger.datetime.datetime")
    def test_log_mood_writes_correct_entry(self, mock_datetime, mock_choice):
        # Mock rationale: fixed emoji and timestamp for deterministic output
        mock_choice.return_value = "😎"
        fixed_dt = datetime.datetime(2023, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = fixed_dt
        # Preserve other datetime constructors
        mock_datetime.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)

        entry = log_mood(self.test_log)
        expected_entry = "2023-01-01 12:00:00 - 😎"
        self.assertEqual(entry, expected_entry)

        # Verify file content matches expected entry
        with self.test_log.open("r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        self.assertEqual(lines, [expected_entry])

    def test_format_entry_uses_provided_datetime(self):
        dt = datetime.datetime(2022, 12, 31, 23, 59, 59)
        entry = format_entry("😀", now=dt)
        self.assertEqual(entry, "2022-12-31 23:59:59 - 😀")

if __name__ == "__main__":
    unittest.main()
