import pytest

# Mock rationale: No external resources are required; we directly test the pure function.
from utils.emoji_clock.src.emoji_clock import time_to_emoji

@pytest.mark.parametrize(
    "hour,minute,expected",
    [
        (0, 0, "\U0001F55B"),   # 12:00 AM → 🕛
        (12, 0, "\U0001F55B"),  # 12:00 PM → 🕛
        (13, 0, "\U0001F550"),  # 13:00 → 1:00 → 🕐
        (13, 14, "\U0001F550"), # 13:14 rounds to 1:00
        (13, 15, "\U0001F55C"), # 13:15 rounds to 1:30
        (13, 44, "\U0001F55C"), # 13:44 rounds to 1:30
        (13, 45, "\U0001F551"), # 13:45 rounds to 2:00
        (23, 59, "\U0001F551"), # 23:59 rounds to 12:00 → 🕛 (but next hour is 0 → 12)
        (11, 30, "\U0001F566"), # 11:30 → 🕦
        (6, 30, "\U0001F561"),  # 6:30 → 🕡
    ],
)
def test_time_to_emoji(hour, minute, expected):
    assert time_to_emoji(hour, minute) == expected

def test_invalid_hour():
    with pytest.raises(ValueError):
        time_to_emoji(-1, 0)
    with pytest.raises(ValueError):
        time_to_emoji(24, 0)

def test_invalid_minute():
    with pytest.raises(ValueError):
        time_to_emoji(10, -5)
    with pytest.raises(ValueError):
        time_to_emoji(10, 60)
