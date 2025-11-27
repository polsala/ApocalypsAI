import datetime

from src.forecast import get_forecast

# Mock rationale: tests are fully deterministic and offline.

def test_forecast_jan_1():
    # 2023‑01‑01 is day 1 → index 0 → ☀️
    date = datetime.date(2023, 1, 1)
    assert get_forecast(date) == "Today's forecast: ☀️"


def test_forecast_jan_2():
    # Day 2 → index 1 → 🌤️
    date = datetime.date(2023, 1, 2)
    assert get_forecast(date) == "Today's forecast: 🌤️"


def test_forecast_dec_31_non_leap():
    # 2023‑12‑31 is day 365 → (365‑1)%9 = 4 → 🌨️
    date = datetime.date(2023, 12, 31)
    assert get_forecast(date) == "Today's forecast: 🌨️"


def test_forecast_leap_year_feb_29():
    # 2024‑02‑29 is day 60 → (60‑1)%9 = 5 → 🌈
    date = datetime.date(2024, 2, 29)
    assert get_forecast(date) == "Today's forecast: 🌈"
