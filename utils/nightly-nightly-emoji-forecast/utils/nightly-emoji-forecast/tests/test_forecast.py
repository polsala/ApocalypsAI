import datetime

# Mock rationale: No external services are called; the function is pure and deterministic.
# Therefore, we can test it directly without any network or filesystem mocks.

from src.forecast import get_emoji_forecast


def test_forecast_known_dates():
    # Known mapping derived from the algorithm in src/forecast.py
    cases = {
        datetime.date(2025, 1, 1): "🌈",   # (ordinal+7) % 10 == 6
        datetime.date(2025, 2, 14): "☁️",  # (ordinal+7) % 10 == 7
        datetime.date(2025, 12, 31): "⛅", # (ordinal+7) % 10 == 2
    }
    for dt, expected in cases.items():
        assert get_emoji_forecast(dt) == expected


def test_forecast_today_consistency():
    today = datetime.date.today()
    first = get_emoji_forecast(today)
    second = get_emoji_forecast(today)
    assert first == second, "Calling the function twice on the same day should yield the same emoji"
