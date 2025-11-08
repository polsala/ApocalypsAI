import sys
from pathlib import Path

# Add the src directory to the import path so we can import emoji_clock directly.
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import pytest
from datetime import datetime
from emoji_clock import get_clock_emoji

@pytest.mark.parametrize(
    "hour,expected",
    [
        (0, "🕛"),
        (1, "🕐"),
        (2, "🕑"),
        (3, "🕒"),
        (4, "🕓"),
        (5, "🕔"),
        (6, "🕕"),
        (7, "🕖"),
        (8, "🕗"),
        (9, "🕘"),
        (10, "🕙"),
        (11, "🕚"),
        (12, "🕛"),
        (13, "🕐"),
        (23, "🕚"),
    ],
)
def test_get_clock_emoji(hour, expected):
    # Mock rationale: we construct a deterministic datetime with the given hour; minutes/seconds are irrelevant.
    dt = datetime(2023, 1, 1, hour, 0, 0)
    assert get_clock_emoji(dt) == expected
