import datetime

from nightly_emoji_forecast.src.forecast import get_forecast


def test_forecast_known_dates():
    """Deterministic checks for a handful of dates.

    The expected strings were generated once and are now hard‑coded.
    Because the algorithm is pure and deterministic, they will never change
    unless the source code is altered.
    """
    cases = {
        datetime.date(2023, 1, 1): "☀️ 🌤️ 🌈",
        datetime.date(2024, 2, 29): "⛈️ 🌧️ 🌨️",  # leap‑year handling
        datetime.date(2025, 12, 31): "🌦️ 🌥️ 🌫️",
        datetime.date(2000, 2, 29): "🌩️ 🌪️ 💨",
    }
    for date, expected in cases.items():
        assert get_forecast(date) == expected


def test_forecast_today_is_consistent():
    """Calling ``get_forecast`` twice for the same date yields the same result.

    # Mock rationale: No network calls; the function is pure, so this test is
    # fully deterministic and offline.
    """
    today = datetime.date.today()
    first = get_forecast(today)
    second = get_forecast(today)
    assert first == second
