import builtins
import io
import pytest

from src.mood_tracker import parse_journal


def test_parse_journal_basic(monkeypatch):
    sample = """2024-10-01 I felt happy and energetic
2024-10-02 It was a sad day
2024-10-03 Nothing much happened"""
    # Mock rationale: replace builtins.open with an in‑memory StringIO returning the sample content
    def mock_open(*args, **kwargs):
        return io.StringIO(sample)
    monkeypatch.setattr(builtins, "open", mock_open)
    result = parse_journal("dummy.txt")
    assert result == {
        "2024-10-01": "😊",
        "2024-10-02": "😞",
        "2024-10-03": "🤔",
    }


def test_parse_journal_ignores_malformed_and_unknown(monkeypatch):
    sample = """2024-10-04 angry about the traffic
malformed line without date
2024-10-05 just a regular day"""
    def mock_open(*args, **kwargs):
        return io.StringIO(sample)
    monkeypatch.setattr(builtins, "open", mock_open)
    result = parse_journal("dummy.txt")
    assert result == {
        "2024-10-04": "😡",
        "2024-10-05": "🤔",
    }
