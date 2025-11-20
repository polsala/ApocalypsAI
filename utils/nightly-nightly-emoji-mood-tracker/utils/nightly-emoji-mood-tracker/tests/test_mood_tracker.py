import os
import tempfile
from src.mood_tracker import MoodTracker


def test_add_and_summary():
    # Use a temporary directory to avoid polluting the real home folder
    with tempfile.TemporaryDirectory() as td:
        storage = os.path.join(td, "data.json")
        tracker = MoodTracker(storage_path=storage)
        # Add two entries with explicit dates (mock rationale: deterministic dates)
        tracker.add_entry("2025-11-20", "😊", "Feeling good")
        tracker.add_entry("2025-11-19", "😢", "A bit sad")
        # Retrieve a 2‑day summary
        summary = tracker.get_summary(days=2)
        assert summary == {"2025-11-20": "😊", "2025-11-19": "😢"}


def test_overwrite_entry():
    with tempfile.TemporaryDirectory() as td:
        storage = os.path.join(td, "data.json")
        tracker = MoodTracker(storage_path=storage)
        tracker.add_entry("2025-11-20", "😊")
        # Overwrite same date with a different emoji
        tracker.add_entry("2025-11-20", "😎", "Cool day")
        summary = tracker.get_summary(days=1)
        assert summary == {"2025-11-20": "😎"}
