import datetime

# Mock rationale: deterministic test using a fixed datetime.
from src.emoji_clock import get_emoji_time


def test_emoji_time_fixed():
    dt = datetime.datetime(2023, 1, 1, 14, 35)  # 2:35 PM
    assert get_emoji_time(dt) == "🕑 3️⃣5️⃣"


def test_midnight():
    dt = datetime.datetime(2023, 1, 1, 0, 0)
    assert get_emoji_time(dt) == "🕛 0️⃣0️⃣"


def test_single_digit_minute():
    dt = datetime.datetime(2023, 1, 1, 9, 5)
    assert get_emoji_time(dt) == "🕘 0️⃣5️⃣"
