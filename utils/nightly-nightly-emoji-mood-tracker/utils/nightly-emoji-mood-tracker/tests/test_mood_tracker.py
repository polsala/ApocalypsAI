import json
import os
import tempfile
from pathlib import Path

import pytest

# Mock rationale: we import the module under test using its relative path.
from utils.nightly_emoji_mood_tracker.src.mood_tracker import (
    add_entry,
    summary,
    _log_path,
    _save_entries,
    _load_entries,
)

@pytest.fixture(autouse=True)
def isolated_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Redirect the log file to a temporary location for each test."""
    temp_log = tmp_path / "test_mood_log.json"
    monkeypatch.setenv("EMOJI_MOOD_LOG", str(temp_log))
    # Ensure a clean start
    if temp_log.exists():
        temp_log.unlink()
    yield
    # Cleanup after test
    if temp_log.exists():
        temp_log.unlink()

def test_add_entry_creates_file_and_writes(monkeypatch: pytest.MonkeyPatch, capsys):
    # Ensure the log file does not exist initially
    assert not _log_path().exists()
    add_entry("😊")
    # File should now exist and contain the emoji
    assert _log_path().is_file()
    data = json.loads(_log_path().read_text(encoding="utf-8"))
    assert data == ["😊"]
    captured = capsys.readouterr()
    assert "Recorded mood: 😊" in captured.out

def test_summary_counts_multiple_entries(isolated_env):
    # Directly save a known list of emojis
    _save_entries(["😊", "😢", "😊", "😎", "😢", "😊"])
    stats = summary()
    assert stats == {"😊": 3, "😢": 2, "😎": 1}

def test_add_entry_invalid_input(monkeypatch: pytest.MonkeyPatch):
    with pytest.raises(ValueError):
        add_entry("")

def test_summary_empty_when_no_file(monkeypatch: pytest.MonkeyPatch):
    # Ensure the log file is absent
    if _log_path().exists():
        _log_path().unlink()
    stats = summary()
    assert stats == {}

def test_load_entries_handles_malformed_json(monkeypatch: pytest.MonkeyPatch):
    # Write malformed JSON to the log file
    _log_path().write_text("{ not: json }", encoding="utf-8")
    entries = _load_entries()
    # Mock rationale: function should recover gracefully and return empty list.
    assert entries == []
