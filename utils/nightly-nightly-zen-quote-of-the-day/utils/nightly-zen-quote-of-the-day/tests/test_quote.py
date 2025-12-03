import datetime
from src.quote import get_quote

def test_known_dates():
    # Mock rationale: Use fixed dates to ensure deterministic output without external calls.
    # 2023-01-01 -> day 1 -> index 0
    date1 = datetime.date(2023, 1, 1)
    assert get_quote(date1) == "The journey of a thousand miles begins with one step."

    # 2023-01-10 -> day 10 -> index 9
    date2 = datetime.date(2023, 1, 10)
    assert get_quote(date2) == "Patience is a bitter plant, but its fruit is sweet."

    # 2023-01-11 -> day 11 -> wraps to index 0 again
    date3 = datetime.date(2023, 1, 11)
    assert get_quote(date3) == "The journey of a thousand miles begins with one step."
