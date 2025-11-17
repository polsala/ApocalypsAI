import datetime
import pytest

# Mock rationale: we replace ``datetime.date.today`` with a fixed date to make the output deterministic.

from src.quote_of_the_day import get_quote


def _mock_today(monkeypatch, mock_date):
    class MockDate(datetime.date):
        @classmethod
        def today(cls):
            return mock_date
    monkeypatch.setattr(datetime, "date", MockDate)


def test_get_quote_without_tag(monkeypatch):
    # Fixed date: 2023-01-01 (ordinal 738156)
    _mock_today(monkeypatch, datetime.date(2023, 1, 1))
    quote = get_quote()
    # There are 5 quotes; 738156 % 5 == 1 -> second quote in the full list
    assert quote == "I have not failed. I've just found 10,000 ways that won't work."


def test_get_quote_with_tag_humor(monkeypatch):
    # Fixed date: 2023-01-02 (ordinal 738157)
    _mock_today(monkeypatch, datetime.date(2023, 1, 2))
    quote = get_quote(tag="humor")
    # Humor quotes: indices 1 and 3 in original list -> list length 2
    # 738157 % 2 == 1 -> second humor quote (index 1)
    assert quote == "If you think you are too small to make a difference, try sleeping with a mosquito."


def test_get_quote_invalid_tag(monkeypatch):
    _mock_today(monkeypatch, datetime.date(2023, 1, 1))
    with pytest.raises(ValueError, match="No quotes found for tag 'nonexistent'"):
        get_quote(tag="nonexistent")
