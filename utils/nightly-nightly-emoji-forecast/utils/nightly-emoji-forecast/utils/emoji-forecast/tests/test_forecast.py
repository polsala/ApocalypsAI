import datetime
from unittest import mock

# Mock rationale: we replace ``datetime.date.today`` to make the test deterministic
# without relying on the actual current date.

from emoji_forecast.src.forecast import get_daily_emoji_forecast


def test_forecast_fixed_date():
    # For the date 2025‑01‑01 the deterministic algorithm should yield the emoji at index 9
    # Calculation (sum of code points): 50+48+50+53+45+48+49+45+48+49 = 485 → 485 % 14 = 9
    # EMOJIS[9] == "🌨️"
    assert get_daily_emoji_forecast("2025-01-01") == "🌨️"


def test_forecast_today_mocked():
    mock_today = datetime.date(2025, 1, 1)
    with mock.patch.object(datetime.date, "today", return_value=mock_today):
        # ``get_daily_emoji_forecast`` with no arguments uses ``datetime.date.today``
        assert get_daily_emoji_forecast() == "🌨️"
