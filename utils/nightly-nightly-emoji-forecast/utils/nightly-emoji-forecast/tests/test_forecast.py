import pytest
from src.forecast import get_emoji_for_date


def test_same_date_consistency():
    """The same valid date should always map to the same emoji."""
    date = "2023-07-04"
    first = get_emoji_for_date(date)
    second = get_emoji_for_date(date)
    assert first == second
    assert first in [
        "☀️", "🌧️", "⛈️", "❄️", "🌪️", "🌈", "☁️", "🌤️", "🌙", "⭐️",
        "🔥", "💧", "🍀", "🍂", "🎉", "🎃", "🎄", "🚀", "🧩", "🤖"
    ]


def test_invalid_date_raises():
    """Providing an invalid date string should raise ValueError."""
    with pytest.raises(ValueError):
        get_emoji_for_date("not-a-date")

# Mock rationale: No external network calls are made; the function is pure and deterministic.
