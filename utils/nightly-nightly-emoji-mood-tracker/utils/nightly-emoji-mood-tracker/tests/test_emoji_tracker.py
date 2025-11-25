import pytest

# Mock rationale: No external services are called; tests are fully deterministic.

from src.emoji_tracker import get_mood_emoji

@pytest.mark.parametrize(
    "text,expected",
    [
        ("I am so happy and joyful today!", "😊"),
        ("Feeling sad and depressed after the news.", "😢"),
        ("I love this new feature!", "❤️"),
        ("I am scared and terrified of the bug.", "😱"),
        ("Just an ordinary day with nothing special.", "😐"),
        ("happy sad", "😐"),  # tie → neutral
        ("", "😐"),  # empty input → neutral
    ],
)
def test_get_mood_emoji(text, expected):
    assert get_mood_emoji(text) == expected
