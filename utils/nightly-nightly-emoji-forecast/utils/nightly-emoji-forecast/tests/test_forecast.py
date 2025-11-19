# Mock rationale: No external services are called; the algorithm is pure.
# The tests therefore remain fully deterministic and offline.

import pytest
from datetime import date

# Import the function under test.
from nightly_emoji_forecast.src.forecast import get_emoji_forecast

# The internal emoji list is part of the contract; we replicate the ordering here
# to compute expected values without importing the private constant.
_WEATHER_EMOJIS = [
    "☀️",
    "🌤️",
    "⛅",
    "🌥️",
    "☁️",
    "🌧️",
    "⛈️",
    "🌩️",
    "❄️",
    "🌪️",
]


def _expected_for(date_obj: date) -> str:
    day_of_year = date_obj.timetuple().tm_yday
    index = day_of_year % len(_WEATHER_EMOJIS)
    return _WEATHER_EMOJIS[index]


@pytest.mark.parametrize(
    "test_date,expected",
    [
        (date(2023, 1, 1), _expected_for(date(2023, 1, 1))),  # day 1 -> index 1
        (date(2023, 12, 31), _expected_for(date(2023, 12, 31))),  # day 365
        (date(2024, 2, 29), _expected_for(date(2024, 2, 29))),  # leap year day 60
        (date(2025, 7, 4), _expected_for(date(2025, 7, 4))),
    ],
)
def test_get_emoji_forecast(test_date, expected):
    assert get_emoji_forecast(test_date) == expected
