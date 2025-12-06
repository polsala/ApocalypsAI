import pytest
from utils.nightly_emoji_mood_tracker.src.emoji_tracker import detect_mood

# Mock rationale: using static strings ensures deterministic offline tests.

def test_positive_mood():
    text = "I love sunny days and feel great"
    assert detect_mood(text) == "😊"


def test_negative_mood():
    text = "I hate rainy weather and feel sad"
    assert detect_mood(text) == "😢"


def test_neutral_mood():
    text = "The day was average with no strong feelings"
    assert detect_mood(text) == "😐"


def test_mixed_mood_equal_counts():
    text = "I love the food but hate the service"
    # love (positive) vs hate (negative) → equal → neutral
    assert detect_mood(text) == "😐"


def test_mixed_mood_negative_dominates():
    text = "I love the view but the traffic made me angry and upset"
    # positives: love (1); negatives: angry, upset (2) → negative
    assert detect_mood(text) == "😢"
