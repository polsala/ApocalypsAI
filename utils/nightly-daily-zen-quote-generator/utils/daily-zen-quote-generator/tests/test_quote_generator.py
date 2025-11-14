import pytest
from datetime import date

# Mock rationale: we replace the internal hash function to make the output deterministic.
from src.quote_generator import get_quote_of_day, _QUOTES


def test_mocked_hash(monkeypatch):
    # Force the hash to return 3, so we expect the 4th quote in the list.
    monkeypatch.setattr("src.quote_generator._hash_date", lambda d: 3)
    test_date = date(1999, 12, 31)
    assert get_quote_of_day(test_date) == _QUOTES[3]
