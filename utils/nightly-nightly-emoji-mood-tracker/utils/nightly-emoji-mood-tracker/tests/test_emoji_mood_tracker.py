# test_emoji_mood_tracker.py
# Deterministic offline tests for the emoji mood tracker utility.
# Mock rationale: No external services are called; the algorithm is pure Python.

import pytest
from src.emoji_mood_tracker import get_mood

@pytest.mark.parametrize(
    "date_str,expected",
    [
        ("2023-01-01", "🥳"),  # Sunday, 20230101 + 6 => index 7
        ("2023-01-02", "😔"),  # Monday, 20230102 + 0 => index 2
        ("2023-01-03", "🤩"),  # Tuesday, 20230103 + 1 => index 4
        ("2025-12-31", "🤩"),  # Computed manually using the same algorithm
    ],
)
def test_get_mood_known_dates(date_str, expected):
    assert get_mood(date_str) == expected


def test_invalid_date_raises():
    with pytest.raises(ValueError):
        get_mood("not-a-date")
