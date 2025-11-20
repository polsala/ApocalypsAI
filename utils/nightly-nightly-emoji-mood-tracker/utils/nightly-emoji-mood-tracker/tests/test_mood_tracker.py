import unittest
import tempfile
from pathlib import Path
from datetime import date, timedelta
import sys

# Mock rationale: using a temporary file ensures deterministic, offline testing without external state.
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from mood_tracker import MoodTracker


class TestMoodTracker(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.storage = Path(self.tmp_dir.name) / "moods.json"
        self.tracker = MoodTracker(self.storage)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_set_and_get_mood(self):
        today = date(2023, 1, 1)
        self.tracker.set_mood(today, "😀")
        self.assertEqual(self.tracker.get_mood(today), "😀")

    def test_most_common(self):
        base = date(2023, 1, 1)
        emojis = ["😀", "😀", "😢", "😀", "😢"]
        for i, e in enumerate(emojis):
            self.tracker.set_mood(base + timedelta(days=i), e)
        self.assertEqual(self.tracker.most_common(), ("😀", 3))

    def test_longest_streak(self):
        # Create two separate streaks: 3 days and 2 days
        dates = [
            date(2023, 1, 1),
            date(2023, 1, 2),
            date(2023, 1, 3),
            date(2023, 1, 5),
            date(2023, 1, 6),
        ]
        for d in dates:
            self.tracker.set_mood(d, "🙂")
        self.assertEqual(self.tracker.longest_streak(), 3)


if __name__ == "__main__":
    unittest.main()
