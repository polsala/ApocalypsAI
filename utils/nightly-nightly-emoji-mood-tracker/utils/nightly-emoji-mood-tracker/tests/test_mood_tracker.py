import sys
from pathlib import Path
import pytest

# Mock rationale: we avoid filesystem I/O by monkeypatching Path.read_text
# to return a predetermined string.

# Adjust sys.path so the src module can be imported without installing a package.
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from mood_tracker import load_moods, most_common_moods, format_summary, main


def test_load_moods_mock(monkeypatch):
    # Mock rationale: simulate a file with several lines, including blanks and spaces.
    mock_content = "Happy\nSad\n  excited\n\nHappy\n"
    def mock_read_text(self):
        return mock_content
    monkeypatch.setattr(Path, "read_text", mock_read_text)
    moods = load_moods(Path("dummy.txt"))
    assert moods == ["happy", "sad", "excited", "happy"]


def test_most_common_moods():
    moods = ["happy", "sad", "happy", "excited", "sad"]
    common = most_common_moods(moods)
    # happy and sad both appear twice, should both be returned
    assert set(common) == {("happy", 2), ("sad", 2)}


def test_format_summary():
    common = [("happy", 3), ("sad", 3)]
    summary = format_summary(common)
    # Order may vary; check both possibilities
    assert summary in {
        "happy 😊 (3), sad 😢 (3)",
        "sad 😢 (3), happy 😊 (3)"
    }


def test_main_success(monkeypatch, capsys):
    # Mock file reading to provide deterministic content.
    mock_content = "happy\nhappy\nsad"
    monkeypatch.setattr(Path, "read_text", lambda self: mock_content)
    # Ensure Path.is_file returns True so load_moods does not raise.
    monkeypatch.setattr(Path, "is_file", lambda self: True)
    exit_code = main(["dummy.txt"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "📈 Mood summary:" in captured.out
    assert "happy 😊 (2)" in captured.out


def test_main_no_file(monkeypatch, capsys):
    # Mock Path.is_file to return False, triggering FileNotFoundError.
    monkeypatch.setattr(Path, "is_file", lambda self: False)
    exit_code = main(["missing.txt"])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Error:" in captured.err
