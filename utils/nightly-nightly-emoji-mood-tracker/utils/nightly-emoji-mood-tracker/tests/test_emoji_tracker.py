import builtins
from unittest import mock

# Mock rationale: ensure deterministic behaviour without external I/O or randomness.

from utils.nightly_emoji_mood_tracker.src.emoji_tracker import get_mood_emoji

def test_happy_keywords():
    assert get_mood_emoji("I am feeling great and wonderful today!") == "😊"
    assert get_mood_emoji("Love this awesome project") == "😊"

def test_sad_keywords():
    assert get_mood_emoji("It was a terrible, sad day.") == "😢"
    assert get_mood_emoji("I feel down and depressed") == "😢"

def test_angry_keywords():
    assert get_mood_emoji("I am so mad and furious about the bug") == "😠"
    assert get_mood_emoji("Annoyed and upset") == "😠"

def test_neutral_when_no_keywords():
    assert get_mood_emoji("Just an ordinary sentence with no mood words.") == "🤔"

def test_override_keyword_lists_via_monkeypatch(monkeypatch):
    # Mock rationale: verify that the function respects the internal keyword lists.
    # Replace the happy list with a custom one and ensure the new keyword triggers the happy emoji.
    custom_happy = ["ecstatic"]
    monkeypatch.setattr(
        "utils.nightly_emoji_mood_tracker.src.emoji_tracker._HAPPY_KEYWORDS",
        custom_happy,
        raising=False,
    )
    assert get_mood_emoji("I am ecstatic about the release") == "😊"
    # Ensure that previous happy keywords no longer trigger (since we replaced the list).
    assert get_mood_emoji("I am happy") != "😊"
