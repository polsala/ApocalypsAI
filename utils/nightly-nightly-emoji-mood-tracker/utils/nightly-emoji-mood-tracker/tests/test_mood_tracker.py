import json
import os
import tempfile
from pathlib import Path

import pytest

# Import the core class from the utility package
from nightly_emoji_mood_tracker.src.mood_tracker import MoodTracker, MOOD_EMOJI_MAP


@pytest.fixture
def temp_tracker():
    """Create a MoodTracker that writes to a temporary file.

    # Mock rationale: Using a temporary directory guarantees isolation from the
    # developer's real ``~/.emoji_mood_tracker.json`` file.
    """
    with tempfile.TemporaryDirectory() as td:
        temp_path = Path(td) / "tracker.json"
        tracker = MoodTracker(data_path=temp_path)
        yield tracker
        # No need to clean – the TemporaryDirectory context does it.


def test_add_and_retrieve_emoji(temp_tracker: MoodTracker):
    # Add a known mood
    temp_tracker.add_entry("2025-11-29", "happy")
    # Directly inspect the persisted JSON to ensure correct storage
    with temp_tracker.data_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    assert data == {"2025-11-29": "happy"}
    # Retrieve the emoji
    assert temp_tracker.get_emoji("2025-11-29") == MOOD_EMOJI_MAP["happy"]
    # Unknown date returns placeholder
    assert temp_tracker.get_emoji("2000-01-01") == "❓"


def test_summary_multiple_entries(temp_tracker: MoodTracker):
    entries = [
        ("2025-11-27", "sad"),
        ("2025-11-28", "neutral"),
        ("2025-11-29", "happy"),
    ]
    for date, mood in entries:
        temp_tracker.add_entry(date, mood)
    # Summary should be sorted chronologically
    expected = f"{MOOD_EMOJI_MAP['sad']} {MOOD_EMOJI_MAP['neutral']} {MOOD_EMOJI_MAP['happy']}"
    assert temp_tracker.summary() == expected


def test_invalid_mood_raises(temp_tracker: MoodTracker):
    with pytest.raises(ValueError) as exc:
        temp_tracker.add_entry("2025-11-30", "ecstatic")
    assert "Unsupported mood" in str(exc.value)


def test_invalid_date_format_raises(temp_tracker: MoodTracker):
    with pytest.raises(ValueError) as exc:
        temp_tracker.add_entry("11-30-2025", "happy")
    assert "date must be in YYYY-MM-DD format" in str(exc.value)
