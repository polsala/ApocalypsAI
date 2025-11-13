import json
from datetime import date
from pathlib import Path

# Mock rationale: we replace the file‑system read with a deterministic in‑memory JSON.
# This ensures the test suite never depends on external files.
MOCK_QUOTES = [
    {"text": "Mocked quote one", "author": "Author A", "tags": ["test"]},
    {"text": "Mocked quote two", "author": "Author B", "tags": ["demo", "test"]},
    {"text": "Mocked quote three", "author": "Author C", "tags": []},
]

# Patch the internal loader to return our mock data.
def _mock_load_quotes(monkeypatch):
    from utils.whimsical-quote-of-the-day.src import quote as qmod
    monkeypatch.setattr(qmod, "_load_quotes", lambda: MOCK_QUOTES)


def test_get_quote_without_tag(monkeypatch):
    _mock_load_quotes(monkeypatch)
    # Mock date to a known day of year (e.g., Jan 2 => day 2)
    mock_today = date(2025, 1, 2)  # day_of_year = 2
    result = __import__("utils.whimsical-quote-of-the-day.src.quote", fromlist=["get_quote"]).get_quote(today=mock_today)
    # day 2 % 3 == 2 -> third quote (index 2)
    assert "Mocked quote three" in result
    assert "Author C" in result


def test_get_quote_with_tag(monkeypatch):
    _mock_load_quotes(monkeypatch)
    mock_today = date(2025, 1, 5)  # day 5
    # Filter by tag "test" – two quotes match.
    result = __import__("utils.whimsical-quote-of-the-day.src.quote", fromlist=["get_quote"]).get_quote(tag="test", today=mock_today)
    # After filtering we have 2 quotes; day 5 % 2 == 1 -> second matching quote.
    assert "Mocked quote two" in result
    assert "Author B" in result


def test_no_quotes_after_filter(monkeypatch):
    _mock_load_quotes(monkeypatch)
    mock_today = date(2025, 1, 1)
    try:
        __import__("utils.whimsical-quote-of-the-day.src.quote", fromlist=["get_quote"]).get_quote(tag="nonexistent", today=mock_today)
    except ValueError as e:
        assert "No quotes available" in str(e)
    else:
        raise AssertionError("Expected ValueError when no quotes match the tag")
