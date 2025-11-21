# test_forecast.py
# Deterministic unit tests for the emoji forecast utility.
# No external resources are required; all data is generated locally.

import datetime

# Mock rationale: we import the function directly; no network calls are made.
from utils.nightly-emoji-forecast.src.forecast import get_emoji_forecast


def test_january_first():
    """January 1st should map to the emoji at index 1 (🌤️)."""
    date = datetime.date(2023, 1, 1)  # non‑leap year, day_of_year = 1
    assert get_emoji_forecast(date) == "🌤️"


def test_december_31st_non_leap():
    """December 31st (non‑leap year) -> day 365 % 12 = 5 -> 🌦️"""
    date = datetime.date(2023, 12, 31)
    assert get_emoji_forecast(date) == "🌦️"


def test_february_29_leap_year():
    """Feb 29 on a leap year (2024) -> day 60 % 12 = 0 -> ☀️"""
    date = datetime.date(2024, 2, 29)
    assert get_emoji_forecast(date) == "☀️"


def test_consistency_across_years():
    """Same day of year should yield same emoji regardless of year.
    Here we compare Jan 15, 2022 (day 15) and Jan 15, 2025 (day 15).
    """
    d1 = datetime.date(2022, 1, 15)
    d2 = datetime.date(2025, 1, 15)
    assert get_emoji_forecast(d1) == get_emoji_forecast(d2)
