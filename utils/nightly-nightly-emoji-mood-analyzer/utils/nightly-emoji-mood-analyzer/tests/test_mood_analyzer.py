# test_mood_analyzer.py
# Deterministic offline tests for the Nightly Emoji Mood Analyzer.
# Mock rationale: No external resources are accessed; all logic is pure Python.

import pytest
from utils.nightly-emoji-mood-analyzer.src.mood_analyzer import analyze_mood

@pytest.mark.parametrize(
    "input_text,expected",
    [
        ("I love this great feature", "😄"),  # happy keywords dominate
        ("This is terrible and I am sad", "😢"),  # sad keywords dominate
        ("Wow, that was amazing!", "😲"),  # surprised category
        ("I am angry and mad about the bug", "😠"),  # angry keywords
        ("Just a regular update with no emotion", "😐"),  # fallback neutral
        ("I love it but also sad about the end", "😄"),  # tie resolved by order (happy first)
        ("bad bad bad happy happy", "😢"),  # more sad hits than happy
    ],
)
def test_analyze_mood(input_text, expected):
    assert analyze_mood(input_text) == expected

def test_non_string_input_raises():
    with pytest.raises(TypeError):
        analyze_mood(123)  # type: ignore[arg-type]
