import json
import os
import tempfile
from datetime import date, timedelta
from pathlib import Path

import pytest

# Import the module under test
from src.mood_tracker import add_entry, summary, _load_data, _save_data, DATA_FILE

# Mock rationale: All file‑system interactions are redirected to a temporary directory
# to keep tests deterministic and offline.

@pytest.fixture(autouse=True)
def isolated_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    # Redirect the data file to the temporary directory
    mock_data_file = tmp_path / "mock_mood.json"
    monkeypatch.setattr("src.mood_tracker.DATA_FILE", mock_data_file)
    # Ensure a clean start for each test
    if mock_data_file.exists():
        mock_data_file.unlink()
    yield
    # Cleanup after test
    if mock_data_file.exists():
        mock_data_file.unlink()

def test_add_entry_creates_new_record():
    created, msg = add_entry("😄")
    assert created is True
    assert "set to 😄" in msg
    data = _load_data()
    assert date.today().isoformat() in data
    assert data[date.today().isoformat()] == "😄"

def test_add_entry_overwrites_existing():
    # First add
    add_entry("😄")
    # Overwrite with a different emoji
    created, msg = add_entry("😢")
    assert created is False  # entry existed, so not "created"
    assert "set to 😢" in msg
    data = _load_data()
    assert data[date.today().isoformat()] == "😢"

def test_summary_counts_correctly():
    # Prepare a series of entries over the last 5 days
    base = date.today()
    emojis = ["😄", "😢", "😄", "🤔", "😄"]
    for i, emoji in enumerate(emojis):
        entry_date = (base - timedelta(days=i)).isoformat()
        add_entry(emoji, entry_date)
    # Request summary for last 5 days
    counts = summary(days=5)
    assert counts == {"😄": 3, "😢": 1, "🤔": 1}

def test_summary_no_entries_returns_empty_dict():
    counts = summary(days=3)
    assert counts == {}

def test_summary_invalid_days_raises():
    with pytest.raises(ValueError):
        summary(days=0)
