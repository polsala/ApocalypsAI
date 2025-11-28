import json
import os
import tempfile
from datetime import date, timedelta

# Mock rationale: we use a temporary file to avoid touching the real user home directory.
# This ensures deterministic, offline tests.

from utils.nightly-emoji-mood_tracker.src.mood_tracker import (
    log_mood,
    get_summary,
    load_db,
    save_db,
    DEFAULT_DB_PATH,
)


def test_log_and_load(tmp_path):
    # Use a temporary db file
    db_file = tmp_path / "mood.json"
    # Log a mood for a fixed date
    fixed_date = date(2023, 1, 1)
    log_mood("😄", today=fixed_date, db_path=db_file)
    # Load and verify
    data = load_db(db_file)
    assert data == {"2023-01-01": "😄"}


def test_summary_multiple_days(tmp_path):
    db_file = tmp_path / "mood.json"
    # Populate several days
    base = date(2023, 1, 10)
    emojis = ["😀", "😐", "😢", "😡"]
    for i, emo in enumerate(emojis):
        day = base - timedelta(days=i)
        log_mood(emo, today=day, db_path=db_file)
    # Request a 3‑day summary ending on base date
    summary = get_summary(days=3, today=base, db_path=db_file)
    expected = [
        {"date": "2023-01-08", "emoji": "😢"},
        {"date": "2023-01-09", "emoji": "😐"},
        {"date": "2023-01-10", "emoji": "😀"},
    ]
    assert summary == expected


def test_save_and_load_consistency(tmp_path):
    db_file = tmp_path / "mood.json"
    sample = {"2022-12-31": "🥳", "2023-01-01": "😎"}
    save_db(sample, db_file)
    loaded = load_db(db_file)
    assert loaded == sample
