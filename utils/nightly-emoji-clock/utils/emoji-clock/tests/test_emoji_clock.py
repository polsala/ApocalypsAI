# Mock rationale: Tests are deterministic and offline; they only exercise pure functions.

import sys
from pathlib import Path

# Add the src directory to sys.path so we can import the module.
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from emoji_clock import get_clock_emoji
import pytest


def test_basic_hours():
    assert get_clock_emoji(0) == "🕛"
    assert get_clock_emoji(1) == "🕐"
    assert get_clock_emoji(12) == "🕛"
    assert get_clock_emoji(13) == "🕐"


def test_wrap_around():
    # Hours beyond 23 should wrap modulo 12 just like normal hours.
    for h in range(24, 48):
        assert get_clock_emoji(h) == get_clock_emoji(h - 24)


def test_invalid_type():
    with pytest.raises(TypeError):
        get_clock_emoji("10")  # type: ignore
