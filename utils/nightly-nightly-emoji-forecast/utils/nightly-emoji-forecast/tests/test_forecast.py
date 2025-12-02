import datetime
from src.forecast import get_forecast

def test_forecast_known_dates():
    # Deterministic expectations for a few fixed dates.
    # The expected strings were generated once and are now hard‑coded.
    cases = {
        datetime.date(2023, 1, 1): "☀️ 🌤️ 🌈",
        datetime.date(2023, 12, 25): "⛈️ 🌨️ 🌈",
        datetime.date(2024, 2, 29): "🌥️ 🌧️ 🌪️",  # Leap‑year handling
    }
    for date, expected in cases.items():
        assert get_forecast(date) == expected, f"Forecast mismatch for {date}"

# Mock rationale: No external services are called; the algorithm is pure Python.
# The test suite runs offline and is fully deterministic.
