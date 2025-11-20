import unittest
from unittest.mock import patch
import os
import json
from datetime import date

# Mock rationale: Ensure tests run offline and deterministically by mocking date.today() and file I/O.

from src.tracker import add_mood, get_mood, summary, LOG_FILE

class TestEmojiMoodTracker(unittest.TestCase):
    def setUp(self):
        # Ensure a clean environment before each test
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)

    def tearDown(self):
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)

    @patch("src.tracker.date")
    def test_add_and_get_mood(self, mock_date):
        mock_date.today.return_value = date(2025, 1, 1)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
        add_mood("😊")
        moods = get_mood()
        self.assertEqual(moods, ["😊"])

    @patch("src.tracker.date")
    def test_multiple_moods_same_day(self, mock_date):
        mock_date.today.return_value = date(2025, 1, 2)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
        add_mood("😊")
        add_mood("😢")
        self.assertEqual(get_mood(), ["😊", "😢"])

    @patch("src.tracker.date")
    def test_summary_counts(self, mock_date):
        mock_date.today.return_value = date(2025, 1, 3)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
        add_mood("😊")
        add_mood("😊")
        add_mood("😢")
        # Simulate a second day
        mock_date.today.return_value = date(2025, 1, 4)
        add_mood("😊")
        summary_result = dict(summary())
        self.assertEqual(summary_result.get("😊"), 3)
        self.assertEqual(summary_result.get("😢"), 1)

    def test_persistence(self):
        # Directly write a known log file and ensure functions read it correctly.
        sample_log = {"2025-01-05": ["🤔", "🤔"], "2025-01-06": ["😂"]}
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(sample_log, f)
        self.assertEqual(get_mood(date(2025, 1, 5)), ["🤔", "🤔"])
        self.assertEqual(dict(summary()), {"🤔": 2, "😂": 1})

if __name__ == "__main__":
    unittest.main()
