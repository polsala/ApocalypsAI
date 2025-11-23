import datetime
from nightly_emoji_mood_tracker import get_mood_emoji

# Mock rationale: The tests rely solely on the deterministic algorithm inside the utility.
# No external services are called, ensuring offline execution.

def test_known_dates():
    # Pre‑computed expected emojis for specific dates using the algorithm.
    cases = {
        datetime.date(2025, 1, 1): "🤔",
        datetime.date(2025, 12, 31): "🥳",
        datetime.date(2020, 2, 29): "😐",
        datetime.date(1999, 12, 31): "🤯",
    }
    for date_obj, expected in cases.items():
        assert get_mood_emoji(date_obj) == expected, f"{date_obj} should map to {expected}"

def test_today_is_consistent():
    today = datetime.date.today()
    first = get_mood_emoji(today)
    second = get_mood_emoji(today)
    assert first == second, "Calling get_mood_emoji multiple times for the same date must be deterministic"
