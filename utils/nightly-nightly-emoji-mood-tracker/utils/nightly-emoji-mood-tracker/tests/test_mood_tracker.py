import json
import pathlib
import tempfile
from unittest import mock

# Mock rationale: We patch ``datetime.date.today`` to a fixed point so that
# ``MoodTracker.get_summary`` produces deterministic results regardless of the
# actual current date when the test suite runs.

from utils.nightly_emoji_mood_tracker.src.mood_tracker import MoodTracker


def _fixed_today():
    return datetime.date(2023, 1, 4)


def test_add_and_summary():
    with tempfile.TemporaryDirectory() as td:
        storage = pathlib.Path(td) / "mood.json"
        tracker = MoodTracker(storage_path=storage)
        # Add three entries spanning three consecutive days.
        tracker.add_entry("2023-01-01", "😊")
        tracker.add_entry("2023-01-02", "😢")
        tracker.add_entry("2023-01-03", "😊")
        # Patch ``datetime.date.today`` to 2023‑01‑04 so the 3‑day window covers
        # 2023‑01‑03, 2023‑01‑02, 2023‑01‑01.
        with mock.patch("datetime.date") as mock_date:
            mock_date.today.return_value = _fixed_today()
            mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
            summary = tracker.get_summary(days=3)
        assert summary == {
            "2023-01-03": "😊",
            "2023-01-02": "😢",
            "2023-01-01": "😊",
        }
        # Verify most_common returns the emoji that appears twice.
        with mock.patch("datetime.date") as mock_date:
            mock_date.today.return_value = _fixed_today()
            mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
            common = tracker.most_common(days=3)
        assert common == "😊"
        # Ensure the JSON file was written correctly.
        with storage.open("r", encoding="utf-8") as f:
            data = json.load(f)
        assert data == {
            "2023-01-01": "😊",
            "2023-01-02": "😢",
            "2023-01-03": "😊",
        }
