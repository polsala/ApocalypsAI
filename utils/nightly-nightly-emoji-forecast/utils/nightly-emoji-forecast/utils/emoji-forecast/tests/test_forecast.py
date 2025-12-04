import datetime
from src.forecast import get_emoji_forecast


def test_emoji_forecast_jan_first():
    # Mock rationale: deterministic mapping ensures offline test.
    date = datetime.date(2023, 1, 1)
    forecast = get_emoji_forecast(date)
    assert forecast == "☀️🥶", f"Unexpected forecast: {forecast}"


def test_emoji_forecast_june_15():
    # Mock rationale: deterministic mapping ensures offline test.
    date = datetime.date(2023, 6, 15)
    forecast = get_emoji_forecast(date)
    # day_of_year = 166 -> weather_idx = (166-1)%5 = 0 -> ☀️
    # pseudo_temp = (166 % 40) - 10 = 6 - 10 = -4 -> 🥶
    assert forecast == "☀️🥶"
