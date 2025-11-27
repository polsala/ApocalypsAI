import json
import os
import tempfile
from pathlib import Path

import pytest

# Mock rationale: we replace the user's home directory with a temporary one so the utility writes to an isolated file.
# This ensures tests are deterministic and offline.

@pytest.fixture
def isolated_home(monkeypatch):
    with tempfile.TemporaryDirectory() as tmpdir:
        fake_home = Path(tmpdir)
        monkeypatch.setattr(Path, "home", lambda: fake_home)
        yield fake_home

def test_log_and_summary(isolated_home):
    from utils.nightly-emoji-mood-tracker.src.mood_tracker import log_mood, summary, DATA_FILE

    # Ensure fresh start
    if DATA_FILE.exists():
        DATA_FILE.unlink()

    # Log three moods on different dates
    log_mood("2024-10-01", "😊")
    log_mood("2024-10-02", "😢")
    log_mood("2024-10-03", "😊")

    # Verify file content directly (deterministic JSON order not required)
    with DATA_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)
    assert data == {
        "2024-10-01": "😊",
        "2024-10-02": "😢",
        "2024-10-03": "😊",
    }

    # Check summary counts
    counter, total = summary()
    assert total == 3
    assert counter["😊"] == 2
    assert counter["😢"] == 1

def test_log_today_defaults_to_utc_date(isolated_home, monkeypatch):
    from utils.nightly-emoji-mood-tracker.src.mood_tracker import log_mood, DATA_FILE
    from datetime import datetime

    # Mock datetime to a known date
    class FixedDatetime(datetime):
        @classmethod
        def utcnow(cls):
            return cls(2025, 1, 15, 12, 0, 0)

    monkeypatch.setattr("datetime.datetime", FixedDatetime)

    # Log without providing a date string
    log_mood("", "🤔")

    with DATA_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)
    assert data == {"2025-01-15": "🤔"}
