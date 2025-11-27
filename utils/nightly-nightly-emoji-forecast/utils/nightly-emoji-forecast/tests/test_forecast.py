import datetime
from unittest import mock

# Mock rationale: we replace the internal seed function to force a known
# deterministic path without relying on the actual SHA‑256 computation.
# This keeps the test offline and fully deterministic.

from src.forecast import get_forecast, _seed_for_date


def test_forecast_with_mocked_seed():
    # Force the seed to a known value (42) regardless of the input date.
    with mock.patch("src.forecast._seed_for_date", return_value=42):
        result = get_forecast(datetime.date(1999, 12, 31))
        # Seed 42 => condition index 42 -> "☁️ Cloudy", precip index 0 -> ""
        assert result == "☁️ Cloudy"


def test_forecast_today_is_deterministic():
    # Use a fixed date to verify that the function returns the same string
    # each time it is called with that date.
    fixed_date = datetime.date(2023, 1, 1)
    first = get_forecast(fixed_date)
    second = get_forecast(fixed_date)
    assert first == second
    # No external network calls – just ensure the string looks plausible.
    assert any(emoji in first for emoji in ["☀️", "⛅", "☁️", "🌧️", "⛈️"])
