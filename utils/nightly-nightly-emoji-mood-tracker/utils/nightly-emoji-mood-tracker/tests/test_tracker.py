import unittest
from unittest.mock import patch
from datetime import date

# Mock rationale: we patch datetime.date.today to ensure deterministic behaviour
# without any network calls or external state.

from utils.nightly-emoji-mood-tracker.src.tracker import MoodTracker, mood_to_emoji

class TestMoodToEmoji(unittest.TestCase):
    def test_known_moods(self):
        self.assertEqual(mood_to_emoji('happy'), '😄')
        self.assertEqual(mood_to_emoji('SAD'), '😢')  # case‑insensitive
        self.assertEqual(mood_to_emoji('unknown'), '🤷')  # fallback

class TestMoodTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = MoodTracker()
        # Add deterministic entries
        self.tracker.add_mood('2025-11-01', 'happy')
        self.tracker.add_mood('2025-11-02', 'tired')
        self.tracker.add_mood('2025-11-03', 'unknown')

    @patch('utils.nightly-emoji-mood-tracker.src.tracker._dt.date')
    def test_summary_within_range(self, mock_date):
        # Mock today to a fixed date to avoid reliance on real clock
        mock_date.fromisoformat.side_effect = lambda s: date.fromisoformat(s)
        summary = self.tracker.get_summary('2025-11-01', '2025-11-02')
        expected = "2025-11-01: 😄\n2025-11-02: 😴"
        self.assertEqual(summary, expected)

    def test_summary_no_entries(self):
        summary = self.tracker.get_summary('2025-10-01', '2025-10-31')
        self.assertEqual(summary, "No entries in the given range.")

    def test_invalid_date_format(self):
        with self.assertRaises(ValueError):
            self.tracker.add_mood('2025/11/01', 'happy')

    def test_start_after_end(self):
        with self.assertRaises(ValueError):
            self.tracker.get_summary('2025-11-05', '2025-11-01')

if __name__ == '__main__':
    unittest.main()
