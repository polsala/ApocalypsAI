import sys
from pathlib import Path

# Mock rationale: No external services; deterministic keyword matching.
# Adjust sys.path so the src module can be imported.
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from emoji_mood import get_mood_emoji

import pytest

@pytest.mark.parametrize(
    "text,expected",
    [
        ("I love this wonderful day!", "😊"),
        ("This is the worst and terrible experience.", "☹️"),
        ("It is an average day.", "😐"),
        ("I am happy but also a bit sad", "😐"),  # equal pos and neg
    ],
)
def test_get_mood_emoji(text, expected):
    assert get_mood_emoji(text) == expected
