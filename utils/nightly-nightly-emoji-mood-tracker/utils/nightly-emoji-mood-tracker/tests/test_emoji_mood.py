import pytest
from src.emoji_mood import get_mood_emoji

# Mock rationale: All test inputs are static strings; no external resources are accessed.

@pytest.mark.parametrize(
    "text,expected",
    [
        ("I am so happy and joyful today!", "😊"),
        ("Feeling sad and down after the loss.", "😢"),
        ("He was angry, furious, and annoyed.", "😠"),
        ("Just an ordinary day with nothing special.", "😐"),
        # Tie between happy and sad keywords should fallback to neutral.
        ("I am happy but also sad.", "😐"),
    ],
)
def test_get_mood_emoji(text, expected):
    assert get_mood_emoji(text) == expected
