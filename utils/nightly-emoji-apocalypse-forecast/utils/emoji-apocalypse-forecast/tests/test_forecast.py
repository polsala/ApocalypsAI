# Tests for the Emoji Apocalypse Forecast utility.
# These tests are fully deterministic and run offline.
# Mock rationale: No external resources are needed; the algorithm is pure Python.

import datetime
import pytest

from utils.emoji_apocalypse_forecast.src.forecast import forecast

# The deterministic emoji list lives inside the module; we replicate the ordering here
# to assert expected outcomes.
_EXPECTED_EMOJIS = [
    "🌞",
    "🌧️",
    "🌩️",
    "🌪️",
    "☄️",
    "🌋",
    "💥",
    "🧨",
    "🪐",
    "🌌",
]


def _checksum(date_str: str) -> int:
    return sum(ord(ch) for ch in date_str)


def _expected_emoji(date_str: str) -> str:
    return _EXPECTED_EMOJIS[_checksum(date_str) % len(_EXPECTED_EMOJIS)]


@pytest.mark.parametrize(
    "date_str",
    [
        "2025-01-01",
        "2025-12-31",
        "1999-07-04",
        "2000-02-29",
    ],
)
def test_known_dates(date_str: str):
    """Validate that known dates map to the expected emoji."""
    assert forecast(date_str) == _expected_emoji(date_str)


def test_today_default():
    """When no argument is supplied, ``forecast`` uses today's date."""
    today = datetime.date.today().isoformat()
    assert forecast() == _expected_emoji(today)


@pytest.mark.parametrize(
    "bad_input",
    [
        "2025/01/01",   # wrong separator
        "01-01-2025",   # wrong order
        "2025-13-01",   # invalid month
        "not-a-date",
        "2025-02-30",   # invalid day
    ],
)
def test_invalid_dates_raise(bad_input: str):
    """Invalid ISO strings should raise ``ValueError``."""
    with pytest.raises(ValueError):
        forecast(bad_input)
