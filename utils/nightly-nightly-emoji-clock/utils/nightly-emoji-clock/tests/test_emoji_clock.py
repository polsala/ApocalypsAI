import pytest
from utils.nightly-emoji-clock.src.emoji_clock import time_to_emoji

# Mock rationale: deterministic offline tests covering edge cases and typical inputs.

@pytest.mark.parametrize(
    "input_time,expected",
    [
        ("00:00", "🕛"),   # midnight
        ("12:00", "🕛"),   # noon
        ("01:15", "🕝"),   # rounds to 1:30
        ("13:45", "🕑"),   # rounds to 14:00 -> 2 o'clock emoji
        ("23:45", "🕛"),   # wraps to midnight
        ("09:20", "🕥"),   # rounds to 9:30
    ],
)
def test_time_to_emoji(input_time, expected):
    assert time_to_emoji(input_time) == expected

def test_invalid_format():
    with pytest.raises(ValueError):
        time_to_emoji("invalid")

def test_out_of_range():
    with pytest.raises(ValueError):
        time_to_emoji("25:00")
