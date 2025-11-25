import builtins
import types
import pytest

# Import the module under test
from src.mood_analyzer import analyze_mood, _load_word_lists

# ---------------------------------------------------------------------------
# Mock rationale: The production word lists are tiny but we want deterministic
# behaviour independent of any future changes.  By monkey‑patching the private
# ``_load_word_lists`` function we can inject a controlled vocabulary.
# ---------------------------------------------------------------------------
@pytest.fixture(autouse=True)
def mock_word_lists(monkeypatch):
    mock_pos = {"happy", "joy", "love"}
    mock_neg = {"sad", "hate", "angry"}
    monkeypatch.setattr(
        "src.mood_analyzer._load_word_lists",
        lambda: (mock_pos, mock_neg),
    )
    yield


def test_positive_mood_returns_happy_emoji():
    text = "I love this happy and joyful day"
    assert analyze_mood(text) == "😊"


def test_negative_mood_returns_sad_emoji():
    text = "I hate this sad and angry situation"
    assert analyze_mood(text) == "😞"


def test_neutral_mood_returns_neutral_emoji_when_counts_equal():
    text = "I love but also hate"
    # One positive (love) and one negative (hate) → neutral
    assert analyze_mood(text) == "😐"


def test_neutral_mood_returns_neutral_emoji_when_no_sentiment_words():
    text = "Just a regular statement without sentiment"
    assert analyze_mood(text) == "😐"

def test_tokenization_is_case_insensitive_and_strips_punctuation():
    text = "Love! LOVE? love..."
    # Three occurrences of the positive word "love"
    assert analyze_mood(text) == "😊"
