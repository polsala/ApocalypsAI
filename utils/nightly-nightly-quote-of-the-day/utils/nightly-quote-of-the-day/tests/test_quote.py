import datetime
from utils.nightly-quote-of-the-day.src.quote import get_quote

def test_known_dates():
    # Mock rationale: fixed dates to ensure deterministic output
    cases = [
        (datetime.date(2023, 1, 1), "The only limit to our realization of tomorrow is our doubts of today. – Franklin D. Roosevelt"),
        (datetime.date(2023, 1, 2), "Life is 10% what happens to us and 90% how we react to it. – Charles R. Swindoll"),
        (datetime.date(2023, 12, 31), "The best way to predict the future is to invent it. – Alan Kay"),
        (datetime.date(2024, 2, 29), "The journey of a thousand miles begins with one step. – Lao Tzu"),
    ]
    for dt, expected in cases:
        assert get_quote(dt) == expected
