# Mock rationale: No external services are used; the algorithm is pure and deterministic.

import datetime
from src.forecast import get_emoji_forecast


def test_known_date_fixed_length():
    """Validate that a known date yields the expected emoji sequence.

    The expected result was pre‑computed using the same algorithm.
    """
    date = datetime.date(2023, 1, 1)
    result = get_emoji_forecast(date, length=4)
    assert result == ["⛅", "🌥️", "☁️", "🌦️"]


def test_default_length_is_three():
    date = datetime.date(2022, 12, 31)
    result = get_emoji_forecast(date)
    assert len(result) == 3


def test_variable_lengths_consistency():
    date = datetime.date(2025, 5, 15)
    short = get_emoji_forecast(date, length=1)
    long = get_emoji_forecast(date, length=5)
    assert len(short) == 1
    assert len(long) == 5
    # The first emoji must be identical regardless of requested length.
    assert short[0] == long[0]
