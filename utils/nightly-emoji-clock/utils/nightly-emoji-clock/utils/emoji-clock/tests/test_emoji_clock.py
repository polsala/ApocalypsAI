import sys
import os
import pytest
from datetime import datetime

# Ensure the src directory is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))

from src.emoji_clock import time_to_emoji, _round_minute


def test_round_minute_basic():
    assert _round_minute(0) == 0
    assert _round_minute(2) == 0
    assert _round_minute(3) == 5
    assert _round_minute(7) == 5
    assert _round_minute(12) == 10
    assert _round_minute(58) == 0  # 58 rounds to 60 → wraps to 0


def test_time_to_emoji_exact_hour():
    dt = datetime(2023, 1, 1, 14, 0)  # 2:00 PM
    assert time_to_emoji(dt) == "🕑🕛"


def test_time_to_emoji_rounded_minutes():
    dt = datetime(2023, 1, 1, 9, 12)  # 9:12 → round to 9:10
    assert time_to_emoji(dt) == "🕘🕑"


def test_time_to_emoji_midnight():
    dt = datetime(2023, 1, 1, 0, 0)  # 12:00 AM
    assert time_to_emoji(dt) == "🕛🕛"

# Mock rationale: No external services are called; all tests are deterministic and run offline.
