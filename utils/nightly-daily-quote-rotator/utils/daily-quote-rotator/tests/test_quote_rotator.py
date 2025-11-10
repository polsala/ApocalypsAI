"""Tests for the daily quote rotator utility."""

import datetime

from src.quote_rotator import get_quote_for_date


def test_known_dates():
    # Mock rationale: using fixed dates ensures deterministic output without external resources.
    # 2023-01-01 → ordinal % 10 = 1 → (1+7)%10 = 8 → quote index 8
    date1 = datetime.date(2023, 1, 1)
    assert get_quote_for_date(date1) == "The journey of a thousand miles begins with one step. – Lao Tzu"

    # 2023-01-02 → ordinal % 10 = 2 → (2+7)%10 = 9 → quote index 9
    date2 = datetime.date(2023, 1, 2)
    assert get_quote_for_date(date2) == "Stay hungry, stay foolish. – Steve Jobs"

    # 2023-01-10 → ordinal % 10 = 0 → (0+7)%10 = 7 → quote index 7
    date3 = datetime.date(2023, 1, 10)
    assert get_quote_for_date(date3) == "What we think, we become. – Buddha"
