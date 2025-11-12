# Mock rationale: All tests are deterministic and run offline; they only depend on the static emoji mapping.

import pytest
from utils.nightly-emoji-mood-analyzer.src.analyzer import analyze_mood

@pytest.mark.parametrize(
    "text,expected",
    [
        ("I am so happy! 😊", "happy"),
        ("Feeling sad today 😢", "sad"),
        ("This makes me angry 😡", "angry"),
        ("No emojis here.", "neutral"),
        ("Mixed feelings 😊😢", "neutral"),  # tie between happy and sad
        ("Lots of joy 😊😊😊", "happy"),
        ("Multiple angry 😡😠🤬", "angry"),
    ],
)
def test_analyze_mood(text, expected):
    assert analyze_mood(text) == expected
