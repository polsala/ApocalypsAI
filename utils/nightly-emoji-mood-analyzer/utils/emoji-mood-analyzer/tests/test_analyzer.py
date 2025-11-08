import pytest
from src.analyzer import analyze_mood

# ---------------------------------------------------------------------------
# Deterministic test cases – no external resources, no randomness.
# ---------------------------------------------------------------------------

def test_happy_emoji_overrides_negative_keyword():
    text = "I hate this 😄"
    # Even though the word "hate" is negative, the happy emoji should dominate.
    assert analyze_mood(text) == "happy"


def test_sad_emoji_overrides_positive_keyword():
    text = "I love this 😢"
    assert analyze_mood(text) == "sad"


def test_keyword_happy_when_no_emoji():
    text = "What a fantastic day"
    assert analyze_mood(text) == "happy"


def test_keyword_sad_when_no_emoji():
    text = "This is the worst experience"
    assert analyze_mood(text) == "sad"


def test_neutral_when_balanced():
    text = "I love it but also hate it"
    # Equal positive and negative keywords → neutral
    assert analyze_mood(text) == "neutral"


def test_neutral_when_no_signal():
    text = "Just a regular statement without emotion"
    assert analyze_mood(text) == "neutral"


def test_invalid_input_type():
    with pytest.raises(TypeError):
        analyze_mood(123)  # type: ignore[arg-type]

# Mock rationale: No external calls are made; all logic is pure and deterministic.
