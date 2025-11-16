import importlib.util
import os
import json
from pathlib import Path

import pytest

# Helper to import the module from its file path after HOME has been monkey‑patched.
def import_mood_tracker(tmp_home):
    module_path = Path(__file__).parents[2] / "src" / "mood_tracker.py"
    spec = importlib.util.spec_from_file_location("mood_tracker", module_path)
    module = importlib.util.module_from_spec(spec)
    # Ensure the module sees the patched HOME when it evaluates DATA_PATH.
    os.environ["HOME"] = str(tmp_home)
    spec.loader.exec_module(module)
    return module


def test_record_creates_file_and_stores_mood(tmp_path, monkeypatch):
    # Mock the HOME directory so the JSON file lands in a temporary location.
    monkeypatch.setenv("HOME", str(tmp_path))
    mood_tracker = import_mood_tracker(tmp_path)

    # Record a mood.
    mood_tracker.record("😊")

    data_file = Path(os.path.expanduser("~/.emoji_mood_tracker.json"))
    assert data_file.is_file(), "Data file should be created after recording"
    with data_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    today = list(data.keys())[0]
    assert data[today] == ["😊"], "Recorded mood should be stored for today"


def test_summary_output(tmp_path, monkeypatch, capsys):
    # Mock HOME and import fresh module.
    monkeypatch.setenv("HOME", str(tmp_path))
    mood_tracker = import_mood_tracker(tmp_path)

    # Record multiple moods.
    mood_tracker.record("😊")
    mood_tracker.record("😢")
    mood_tracker.record("😊")

    # Capture summary output.
    mood_tracker.summary()
    captured = capsys.readouterr()
    # Expected counts: 😊 appears twice, 😢 once.
    assert "😊: 2" in captured.out
    assert "😢: 1" in captured.out


def test_summary_no_data(tmp_path, monkeypatch, capsys):
    # Ensure no data file exists.
    monkeypatch.setenv("HOME", str(tmp_path))
    mood_tracker = import_mood_tracker(tmp_path)
    # Directly call summary without any recordings.
    mood_tracker.summary()
    captured = capsys.readouterr()
    assert "No moods recorded yet." in captured.out
