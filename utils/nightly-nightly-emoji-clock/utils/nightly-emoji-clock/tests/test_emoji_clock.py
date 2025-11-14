"""Tests for the Emoji Clock utility."""

import sys
import pathlib
import datetime
from unittest.mock import patch

# Add the src directory to the import path so we can import ``emoji_clock``
src_dir = pathlib.Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(src_dir))

from emoji_clock import get_emoji_time


class FixedNow(datetime.datetime):
    """datetime subclass that returns a fixed ``now()`` value."""

    @classmethod
    def now(cls):
        # 2023‑01‑01 14:05 → hour 2, minute <30 → 🕑
        return cls(2023, 1, 1, 14, 5)


def test_hour_emoji():
    with patch("emoji_clock.datetime", FixedNow):
        assert get_emoji_time() == "🕑 14:05"


class FixedNowHalf(datetime.datetime):
    @classmethod
    def now(cls):
        # 2023‑01‑01 14:45 → hour 2, minute >=30 → 🕝
        return cls(2023, 1, 1, 14, 45)


def test_half_hour_emoji():
    with patch("emoji_clock.datetime", FixedNowHalf):
        assert get_emoji_time() == "🕝 14:45"


def test_explicit_datetime():
    # Directly pass a datetime without mocking
    dt = datetime.datetime(2023, 1, 1, 23, 59)
    # 23:59 → hour 11 (23 % 12 = 11), minute >=30 → 🕦
    assert get_emoji_time(dt) == "🕦 23:59"
