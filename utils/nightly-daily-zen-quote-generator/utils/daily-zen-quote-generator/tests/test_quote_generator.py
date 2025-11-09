import datetime
import pathlib
import json
import sys
import pytest

# Mock rationale: we replace datetime.date.today to control the date.
class MockDate(datetime.date):
    @classmethod
    def today(cls):
        return cls(2023, 3, 14)  # Pi Day

def test_quote_of_the_day(monkeypatch):
    # Apply mock
    monkeypatch.setattr(datetime, "date", MockDate)

    # Ensure src is on path
    src_path = pathlib.Path(__file__).parents[1] / "src"
    sys.path.append(str(src_path))

    from quote_generator import quote_of_the_day, load_quotes

    expected_index = (MockDate(2023, 3, 14).timetuple().tm_yday - 1) % 5
    quotes = load_quotes()
    expected_quote = quotes[expected_index]

    assert quote_of_the_day() == expected_quote

def test_load_quotes():
    src_path = pathlib.Path(__file__).parents[1] / "src"
    sys.path.append(str(src_path))

    from quote_generator import load_quotes

    quotes = load_quotes()
    assert isinstance(quotes, list)
    assert len(quotes) == 5
    assert all(isinstance(q, str) for q in quotes)
