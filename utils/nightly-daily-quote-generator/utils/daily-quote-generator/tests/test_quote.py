"""Tests for the daily quote generator."""

import datetime
from unittest import mock
import importlib.util
import pathlib


def _load_quote_module():
    """Load the quote module from its file path using importlib."""
    module_path = pathlib.Path(__file__).resolve().parents[2] / "src" / "quote.py"
    spec = importlib.util.spec_from_file_location("quote", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_get_daily_quote_deterministic():
    # Mock rationale: Fix today's date to ensure deterministic output.
    fixed_date = datetime.date(2023, 1, 15)  # Arbitrary fixed date
    quote = _load_quote_module()
    with mock.patch.object(datetime.date, "today", return_value=fixed_date):
        result = quote.get_daily_quote()
        quotes = quote._load_quotes()
        index = fixed_date.toordinal() % len(quotes)
        expected = quotes[index]
        assert result == expected
