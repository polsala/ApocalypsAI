import pytest
from datetime import date

# Import the function under test
from src.forecast import get_forecast

# Mapping used internally – duplicated here for test expectations
_EMOJI_MAP = ["☀️", "🌤️", "🌧️", "⛈️"]

@pytest.mark.parametrize(
    "test_date,expected_index",
    [
        (date(2025, 1, 1), (date(2025, 1, 1).toordinal() % 4)),
        (date(2000, 2, 29), (date(2000, 2, 29).toordinal() % 4)),
        (date(1999, 12, 31), (date(1999, 12, 31).toordinal() % 4)),
        (date(1970, 1, 1), (date(1970, 1, 1).toordinal() % 4)),
    ],
)
def test_forecast_deterministic(test_date, expected_index):
    """Ensure the forecast is deterministic and matches the internal mapping.

    # Mock rationale: No external services are called; the function is pure.
    """
    expected_emoji = _EMOJI_MAP[expected_index]
    assert get_forecast(test_date) == expected_emoji

def test_forecast_known_dates():
    """Validate a few hard‑coded dates against their expected emojis.

    # Mock rationale: Using known ordinal values to guarantee reproducibility.
    """
    # 2025‑12‑25 → ordinal % 4 = ?
    d = date(2025, 12, 25)
    idx = d.toordinal() % 4
    assert get_forecast(d) == _EMOJI_MAP[idx]

    # 2020‑02‑29 (leap day)
    d = date(2020, 2, 29)
    idx = d.toordinal() % 4
    assert get_forecast(d) == _EMOJI_MAP[idx]
